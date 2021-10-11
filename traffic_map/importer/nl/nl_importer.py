from traffic_map.importer.base_importer import BaseImporter

# http://opendata.ndw.nu/
from traffic_map.importer.nl.nl_accidents_importer import get_accidents, namespaces
from traffic_map.models import RoadAccident


class NetherlandsImporter(BaseImporter):
    def __init__(self, cycleId):
        self.CycleId = cycleId

    def load_accidents(self):
        accidents = get_accidents()
        for accident in accidents:
            record = accident.find("./d2lm:situationRecord", namespaces)
            acc_type = record.attrib['{{{ns}}}{key}'.format(ns=namespaces['xsi'], key="type")]
            descr = acc_type
            if acc_type == 'VehicleObstruction':
                descr = record.find("./d2lm:vehicleObstructionType", namespaces).text
            elif acc_type == 'Accident':
                descr = record.find("./d2lm:accidentType", namespaces).text

            RoadAccident(refresh_cycle=self.CycleId,
                         loc_latitude=record.find("./d2lm:groupOfLocations/d2lm:locationForDisplay/d2lm:latitude",
                                                  namespaces).text,
                         loc_longitude=record.find("./d2lm:groupOfLocations/d2lm:locationForDisplay/d2lm:longitude",
                                                   namespaces).text,
                         created_at=record.find("./d2lm:situationRecordCreationTime", namespaces).text,
                         title=acc_type,
                         description=descr).save()
