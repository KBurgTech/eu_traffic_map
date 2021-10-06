from django.http import HttpResponse

from traffic_map.service.update_service import run_import


def do_import(request):
    run_import()
    return HttpResponse()