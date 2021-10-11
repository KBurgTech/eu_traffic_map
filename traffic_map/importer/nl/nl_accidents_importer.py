from traffic_map.importer.nl.helper import download_file, extract_gz_to_string, string_to_xml

FILE_URL = "http://opendata.ndw.nu/incidents.xml.gz"
namespaces = {
    'SOAP': 'http://schemas.xmlsoap.org/soap/envelope/',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    'd2lm': 'http://datex2.eu/schema/2/2_0'
}


def get_accidents():
    download = download_file(FILE_URL)
    string = extract_gz_to_string(download)
    xml = string_to_xml(string)
    accidents = xml.findall("./SOAP:Body/d2lm:d2LogicalModel/d2lm:payloadPublication/d2lm:situation", namespaces)
    return accidents
