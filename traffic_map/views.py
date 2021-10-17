from django.http import HttpResponse
from django.template import loader

from traffic_map.models import MLPrediction, RefreshCycle
from traffic_map.service.update_service import get_current_cycle
from traffic_map.ui.views import mapView


def main_view(request):
    return mapView.map_view_main(request)


def index_view(request):
    template = loader.get_template('Index.html')
    context = {'map': mapView.map_view_main(), 'current_cycle': RefreshCycle.objects.filter(id=get_current_cycle())[0]}
    return HttpResponse(template.render(context, request))


def ml_trainer_view(request, cycle_id):
    template = loader.get_template('MLTrainer.html')
    cycle_info = {
        'allowed_runs': RefreshCycle.objects.filter(finished=True, status=1).values_list('id', flat=True),
        'current': RefreshCycle.objects.filter(id=cycle_id)[0],
        'latest': get_current_cycle()
    }
    context = {'data': MLPrediction.objects.filter(refresh_cycle=cycle_id), 'cycleInfo': cycle_info}
    return HttpResponse(template.render(context, request))
