from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from traffic_map.ui.views import mapView


def main_view(request):
    return mapView.map_view_main(request)
