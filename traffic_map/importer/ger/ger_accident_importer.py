import requests

BASE_URL = "https://verkehr.autobahn.de/o/autobahn"
URL_ROADS = BASE_URL + "/"
URL_ROADWORKS = "/services/warning"


def load_warnings_for_road(motorway):
    try:
        response = requests.get(BASE_URL + "/" + motorway + URL_ROADWORKS)
        if response is None or not response.ok:
            return
        json = response.json()
        if json is not None:
            return json['warning']
    except Exception as e:
        print(e)

