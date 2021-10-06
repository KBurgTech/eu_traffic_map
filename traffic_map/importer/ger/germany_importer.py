import requests

from traffic_map.importer.base_importer import BaseImporter
from traffic_map.models import Roadwork

BASE_URL = "https://verkehr.autobahn.de/o/autobahn"
URL_ROADS = BASE_URL + "/"
URL_ROADWORKS = "/services/roadworks"


def load_roadwork_for_road(motorway):
    try:
        response = requests.get(BASE_URL + "/" + motorway + URL_ROADWORKS)
        if response is None or not response.ok:
            return
        json = response.json()
        if json is not None:
            return json['roadworks']
    except Exception as e:
        print(e)


def get_roads() -> list:
    response = requests.get(URL_ROADS)
    return response.json()['roads']


class GermanyImporter(BaseImporter):

    def __init__(self, cycleId):
        self.CycleId = cycleId

    def load_roadwork(self):
        print("Loading German roadwork data...")
        self.load_roadworks()

    def load_roadworks(self):
        for road in get_roads():
            roadworks = load_roadwork_for_road(road)
            if roadworks is not None:
                for work in roadworks:
                    Roadwork(refresh_cycle=self.CycleId,
                             loc_latitude=work['coordinate']['lat'],
                             loc_longitude=work['coordinate']['long'],
                             created_at=work['startTimestamp'],
                             title=work['title'],
                             description=''.join(work['description'])).save()
