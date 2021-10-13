from traffic_map.importer.nl.helper import download_file, extract_gz_to_string, string_to_xml, NL_XML_NAMESPACES

FILE_URL = "http://opendata.ndw.nu/incidents.xml.gz"


def get_accidents():
    download = download_file(FILE_URL)
    string = extract_gz_to_string(download)
    xml = string_to_xml(string)
    accidents = xml.findall("./SOAP:Body/d2lm:d2LogicalModel/d2lm:payloadPublication/d2lm:situation", NL_XML_NAMESPACES)
    return accidents
