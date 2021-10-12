from django.core import serializers
from django.http import HttpResponse, JsonResponse

from traffic_map.models import RoadAccident, Roadwork, LiveItem


def get_accidents(request):
    serialized_obj = serializers.serialize('json', RoadAccident.objects.all())
    return HttpResponse(serialized_obj, content_type="application/json")


def get_roadworks(request):
    serialized_obj = serializers.serialize('json', Roadwork.objects.all())
    return HttpResponse(serialized_obj, content_type="application/json")


def get_liveitems(request):
    serialized_obj = serializers.serialize('json', LiveItem.objects.all())
    return HttpResponse(serialized_obj, content_type="application/json")
