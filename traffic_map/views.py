from django.http import HttpResponse
from django.template import loader

from traffic_map.models import MLPrediction
from traffic_map.service.update_service import get_current_cycle
from traffic_map.ui.views import mapView


def main_view(request):
    return mapView.map_view_main(request)


def index_view(request):
    template = loader.get_template('Index.html')
    context = {'map': mapView.map_view_main()}
    return HttpResponse(template.render(context, request))


def ml_trainer_view(request):
    template = loader.get_template('MLTrainer.html')
    context = {'data': MLPrediction.objects.filter(refresh_cycle=get_current_cycle())}
    return HttpResponse(template.render(context, request))
