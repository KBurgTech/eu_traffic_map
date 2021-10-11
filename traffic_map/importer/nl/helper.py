import gzip
import io
import xml.etree.ElementTree

import requests


def download_file(url):
    request = requests.get(url)
    return io.BytesIO(request.content)


def extract_gz_to_string(content):
    return gzip.GzipFile(fileobj=content, mode="rb").read().decode("utf-8")


def string_to_xml(content):
    return xml.etree.ElementTree.fromstring(content)
