import requests

from traffic_map.importer.base_importer import BaseImporter
from traffic_map.importer.ger.ger_accident_importer import load_warnings_for_road
from traffic_map.importer.ger.ger_roadwork_importer import load_roadwork_for_road
from traffic_map.importer.ger.ger_webcam_importer import load_webcams_for_road
from traffic_map.models import Roadwork, RoadAccident, LiveItem

BASE_URL = "https://verkehr.autobahn.de/o/autobahn"
URL_ROADS = BASE_URL + "/"
URL_ROADWORKS = "/services/roadworks"


def get_roads() -> list:
    response = requests.get(URL_ROADS)
    return response.json()['roads']


class GermanyImporter(BaseImporter):

    def __init__(self, cycleId):
        self.CycleId = cycleId
        self.roads = None

    def load_all(self):
        self.roads = get_roads()
        self.load_roadwork()
        self.load_accidents()
        self.load_liveitems()

    def load_liveitems(self):
        if self.roads is None:
            self.roads = get_roads()
        for road in self.roads:
            webcams = load_webcams_for_road(road)
            if webcams is not None:
                for webcam in webcams:
                    data = webcam['linkurl']
                    l_type = 'l_video'
                    if data is None or data == '':
                        if webcam['imageurl'] is None or webcam['imageurl'] == '':
                            continue
                        else:
                            data = webcam['imageurl']
                            l_type = 'l_image'

                    LiveItem(refresh_cycle=self.CycleId,
                             loc_latitude=webcam['coordinate']['lat'],
                             loc_longitude=webcam['coordinate']['long'],
                             title=webcam['title'],
                             type=l_type,
                             data=data).save()

    def load_accidents(self):
        if self.roads is None:
            self.roads = get_roads()
        for road in self.roads:
            warnings = load_warnings_for_road(road)
            if warnings is not None:
                for warning in warnings:
                    RoadAccident(refresh_cycle=self.CycleId,
                                 loc_latitude=warning['coordinate']['lat'],
                                 loc_longitude=warning['coordinate']['long'],
                                 created_at=warning['startTimestamp'],
                                 title=warning['title'],
                                 description=''.join(warning['description'])).save()

    def load_roadwork(self):
        if self.roads is None:
            self.roads = get_roads()
        for road in self.roads:
            roadworks = load_roadwork_for_road(road)
            if roadworks is not None:
                for work in roadworks:
                    Roadwork(refresh_cycle=self.CycleId,
                             loc_latitude=work['coordinate']['lat'],
                             loc_longitude=work['coordinate']['long'],
                             created_at=work['startTimestamp'],
                             title=work['title'],
                             type=work['display_type'],
                             description=''.join(work['description'])).save()
