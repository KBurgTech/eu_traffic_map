import re

import folium
from branca.element import Element, CssLink, JavascriptLink
from django.db.models import Max
from folium import plugins

from traffic_map.models import Roadwork, RoadAccident, LiveItem

pattern = re.compile('[\W_]+')


def add_roadwork(m):
    current_cycle = Roadwork.objects.aggregate(Max('refresh_cycle'))['refresh_cycle__max']
    for work in Roadwork.objects.filter(refresh_cycle=current_cycle):
        folium.Marker(
            location=[work.loc_latitude, work.loc_longitude],
            popup=pattern.sub('', work.description),  # TODO REMOVE WEIRD FIX
            icon=folium.Icon(icon='road', color='orange')
        ).add_to(m)


def add_accidents(m):
    current_cycle = RoadAccident.objects.aggregate(Max('refresh_cycle'))['refresh_cycle__max']
    for accident in RoadAccident.objects.filter(refresh_cycle=current_cycle):
        folium.Marker(
            location=[accident.loc_latitude, accident.loc_longitude],
            popup=pattern.sub('', accident.title),  # TODO REMOVE WEIRD FIX
            icon=folium.Icon(icon='info-sign', color='red')
        ).add_to(m)


def add_liveitem(m):
    current_cycle = LiveItem.objects.aggregate(Max('refresh_cycle'))['refresh_cycle__max']
    for item in LiveItem.objects.filter(refresh_cycle=current_cycle):
        folium.Marker(
            location=[item.loc_latitude, item.loc_longitude],
            popup='<div><h4>{title}</h4><iframe src="{link}"></iframe></div>'.format(link=item.data, title=item.title),
            # TODO REMOVE WEIRD FIX
            icon=folium.Icon(icon='camera', color='blue')
        ).add_to(m)


def map_view_main():
    figure = folium.Figure(width='100%', height='100%')
    m = folium.Map(
        width='100%', height='100%',
        location=[51.680408, 7.815184],
        zoom_start=6,
        tiles='OpenStreetMap'
    )
    cluster = plugins.MarkerCluster().add_to(m) #Inject MarkerCluster
    m.add_to(figure)

    js_intercept = '''
    var mapsPlaceholder = [];
    L.Map.addInitHook(function () {
      mapsPlaceholder.push(this); // Use whatever global scope variable you like.
    });
    '''
    m.get_root().script.add_child(Element(js_intercept))
    m = m._repr_html_()
    return m
