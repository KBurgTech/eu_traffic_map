import datetime

from traffic_map.importer.nl.helper import download_file, extract_gz_to_string, string_to_xml, NL_XML_NAMESPACES

FILE_URL = "http://opendata.ndw.nu/wegwerkzaamheden.xml.gz"


# MaintenanceWorks
# ReroutingManagement
# ConstructionWorks
# PublicEvent
# RoadOrCarriagewayOrLaneManagement


def get_roadworks():
    download = download_file(FILE_URL)
    string = extract_gz_to_string(download)
    xml = string_to_xml(string)
    items = xml.findall("./SOAP:Body/d2lm:d2LogicalModel/d2lm:payloadPublication/d2lm:situation", NL_XML_NAMESPACES)
    for item in items:
        is_current(item.find("./d2lm:situationRecord", NL_XML_NAMESPACES))
    return items


def is_current(record):
    validity = record.find("./d2lm:validity/d2lm:validityTimeSpecification", NL_XML_NAMESPACES)
    start = validity.find("./d2lm:overallStartTime", NL_XML_NAMESPACES)
    end = validity.find("./d2lm:overallEndTime", NL_XML_NAMESPACES)
    if start is None or end is None:
        return False

    start_d = datetime.datetime.strptime(start.text, '%Y-%m-%dT%H:%M:%SZ')
    end_d = datetime.datetime.strptime(end.text, '%Y-%m-%dT%H:%M:%SZ')

    return start_d < datetime.datetime.now() < end_d
