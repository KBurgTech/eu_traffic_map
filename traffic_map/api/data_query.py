from django.core import serializers
from django.http import HttpResponse, JsonResponse

from traffic_map.models import RoadAccident, Roadwork, LiveItem
from traffic_map.service.update_service import get_current_cycle


def get_accidents(request):
    serialized_obj = serializers.serialize('json', RoadAccident.objects.filter(refresh_cycle=get_current_cycle()))
    return HttpResponse(serialized_obj, content_type="application/json")


def get_roadworks(request):
    serialized_obj = serializers.serialize('json', Roadwork.objects.filter(refresh_cycle=get_current_cycle()))
    return HttpResponse(serialized_obj, content_type="application/json")


def get_liveitems(request):
    serialized_obj = serializers.serialize('json', LiveItem.objects.filter(refresh_cycle=get_current_cycle()))
    return HttpResponse(serialized_obj, content_type="application/json")
