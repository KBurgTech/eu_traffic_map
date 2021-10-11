from django.http import HttpResponse
from django.template import loader

from traffic_map.ui.views import mapView


def main_view(request):
    return mapView.map_view_main(request)


def index_view(request):
    template = loader.get_template('Index.html')
    context = {'TestVar': "Loool"}
    return HttpResponse(template.render(context, request))
