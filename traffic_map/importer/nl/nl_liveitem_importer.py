from traffic_map.importer.nl.helper import download_file, extract_gz_to_string, string_to_xml, NL_XML_NAMESPACES

FILE_URL = "http://opendata.ndw.nu/DRIPS.xml.gz"
BOARD_INFO_URL = "http://opendata.ndw.nu/LocatietabelDRIPS.xml.gz"


def get_liveitems():
    download = download_file(FILE_URL)
    string = extract_gz_to_string(download)
    xml = string_to_xml(string)
    items = xml.findall("./SOAP:Body/d2lm:d2LogicalModel/d2lm:payloadPublication/d2lm:vmsUnit", NL_XML_NAMESPACES)
    return items


def get_boards():
    download = download_file(BOARD_INFO_URL)
    string = extract_gz_to_string(download)
    xml = string_to_xml(string)
    boards = xml.findall(
        "./SOAP:Body/d2lm:d2LogicalModel/d2lm:payloadPublication/d2lm:vmsUnitTable/d2lm:vmsUnitRecord",
        NL_XML_NAMESPACES)

    board_dict = {}
    for board in boards:
        if board.find("./d2lm:vmsRecord/d2lm:vmsRecord/d2lm:vmsLocation/d2lm:locationForDisplay", NL_XML_NAMESPACES) is None: #NO LOCATION DATA = IGNORE
            continue
        board_data = {
            'title': board.find("./d2lm:vmsRecord/d2lm:vmsRecord/d2lm:vmsDescription/d2lm:values/d2lm:value", NL_XML_NAMESPACES).text,
            'lat': board.find(
                "./d2lm:vmsRecord/d2lm:vmsRecord/d2lm:vmsLocation/d2lm:locationForDisplay/d2lm:latitude", NL_XML_NAMESPACES).text,
            'long': board.find(
                "./d2lm:vmsRecord/d2lm:vmsRecord/d2lm:vmsLocation/d2lm:locationForDisplay/d2lm:longitude", NL_XML_NAMESPACES).text}
        board_dict[board.attrib['id']] = board_data

    return board_dict
