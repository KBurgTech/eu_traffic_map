from traffic_map.importer.base_importer import BaseImporter

# http://opendata.ndw.nu/
from traffic_map.importer.nl.nl_accidents_importer import get_accidents, NL_XML_NAMESPACES
from traffic_map.importer.nl.nl_liveitem_importer import get_liveitems, get_boards
from traffic_map.importer.nl.nl_roadwork_importer import get_roadworks, is_current
from traffic_map.models import RoadAccident, LiveItem, Roadwork, MLPrediction
from traffic_map.service import ml
from traffic_map.service.ml import MODEL_PATH


class NetherlandsImporter(BaseImporter):
    def __init__(self, cycleId):
        self.CycleId = cycleId

    def load_roadwork(self):
        works = get_roadworks()
        for work in works:
            record = work.find("./d2lm:situationRecord", NL_XML_NAMESPACES)
            w_type = record.attrib['{{{ns}}}{key}'.format(ns=NL_XML_NAMESPACES['xsi'], key="type")]
            if w_type != "MaintenanceWorks" and w_type != "ConstructionWorks":
                continue
            if not is_current(record):
                continue
            location = record.find(
                "./d2lm:groupOfLocations/d2lm:locationContainedInItinerary/d2lm:location/d2lm:locationForDisplay",
                NL_XML_NAMESPACES)
            if location is None:
                location = record.find(
                    "./d2lm:groupOfLocations/d2lm:locationContainedInItinerary/d2lm:location/d2lm:pointByCoordinates/d2lm:pointCoordinates",
                    NL_XML_NAMESPACES)
            if location is None:
                continue
            created_at = work.find("./d2lm:situationVersionTime", NL_XML_NAMESPACES).text
            descr = ""
            if w_type == "MaintenanceWorks":
                descr = record.find("./d2lm:roadMaintenanceType", NL_XML_NAMESPACES).text
            elif w_type == "ConstructionWorks":
                descr = record.find("./d2lm:constructionWorkType", NL_XML_NAMESPACES).text

            Roadwork(refresh_cycle=self.CycleId,
                     loc_latitude=location.find("./d2lm:latitude", NL_XML_NAMESPACES).text,
                     loc_longitude=location.find("./d2lm:longitude", NL_XML_NAMESPACES).text,
                     created_at=created_at,
                     title=w_type,
                     type=w_type,
                     description=descr).save()

    def load_liveitems(self):
        liveitems = get_liveitems()
        boards = get_boards()
        ml_model = ml.load_model(MODEL_PATH)
        for item in liveitems:
            record = item.find("./d2lm:vms/d2lm:vms/d2lm:vmsMessage/d2lm:vmsMessage", NL_XML_NAMESPACES)
            board_id = item.find("./d2lm:vmsUnitReference", NL_XML_NAMESPACES).attrib['id']
            if record.find("./d2lm:vmsMessageExtension", NL_XML_NAMESPACES) is None or board_id not in boards:
                continue
            image_data = record.find("./d2lm:vmsMessageExtension/d2lm:vmsMessageExtension/d2lm:vmsImage/d2lm:imageData",
                                     NL_XML_NAMESPACES)
            img_binary = image_data.find("./d2lm:binary", NL_XML_NAMESPACES).text
            ml_score = ml_model.predict([ml.get_predict_data(img_binary)])

            MLPrediction(refresh_cycle=self.CycleId, data=img_binary, score=ml_score, is_blank=ml_score > 0.50).save()
            if ml_score > 0.50:
                continue

            LiveItem(refresh_cycle=self.CycleId,
                     loc_latitude=boards[board_id]['lat'],
                     loc_longitude=boards[board_id]['long'],
                     title=boards[board_id]['title'],
                     type="b_img",
                     data="data:{img_type};{enc},{data}".format(
                         img_type=image_data.find("./d2lm:mimeType", NL_XML_NAMESPACES).text,
                         enc=image_data.find("./d2lm:encoding", NL_XML_NAMESPACES).text,
                         data=img_binary)
                     ).save()

    def load_accidents(self):
        accidents = get_accidents()
        for accident in accidents:
            record = accident.find("./d2lm:situationRecord", NL_XML_NAMESPACES)
            acc_type = record.attrib['{{{ns}}}{key}'.format(ns=NL_XML_NAMESPACES['xsi'], key="type")]
            descr = acc_type
            if acc_type == 'VehicleObstruction':
                descr = record.find("./d2lm:vehicleObstructionType", NL_XML_NAMESPACES).text
            elif acc_type == 'Accident':
                descr = record.find("./d2lm:accidentType", NL_XML_NAMESPACES).text

            RoadAccident(refresh_cycle=self.CycleId,
                         loc_latitude=record.find("./d2lm:groupOfLocations/d2lm:locationForDisplay/d2lm:latitude",
                                                  NL_XML_NAMESPACES).text,
                         loc_longitude=record.find("./d2lm:groupOfLocations/d2lm:locationForDisplay/d2lm:longitude",
                                                   NL_XML_NAMESPACES).text,
                         created_at=record.find("./d2lm:situationRecordCreationTime", NL_XML_NAMESPACES).text,
                         title=acc_type,
                         description=descr).save()
