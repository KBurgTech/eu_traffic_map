import re;

import folium
from django.db.models import Max
from django.http import HttpResponse
from django.template import loader

from traffic_map.models import Roadwork

pattern = re.compile('[\W_]+')


def add_roadwork(m):
    max_rating = Roadwork.objects.aggregate(Max('refresh_cycle'))['refresh_cycle__max']
    for work in Roadwork.objects.filter(refresh_cycle=max_rating):
        folium.Marker(
            location=[work.loc_latitude, work.loc_longitude],
            popup=pattern.sub('', work.description),  # TODO REMOVE WEIRD FIX
            icon=folium.Icon(icon='road', color='orange')
        ).add_to(m)


def map_view_main(request):
    figure = folium.Figure(width='100%', height='100%')
    m = folium.Map(
        width='100%', height='100%',
        location=[52.261350, 4.943192],
        zoom_start=12,
        tiles='OpenStreetMap'
    )
    m.add_to(figure)
    folium.Marker(
        location=[52.260350, 4.958292],
        popup='CCTV Camera',
        icon=folium.Icon(icon='camera', color='black')
    ).add_to(m)

    add_roadwork(m)
    m = figure._repr_html_()
    template = loader.get_template('MapView.html')
    context = {'map': m}
    return HttpResponse(template.render(context, request))
