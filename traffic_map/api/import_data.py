import threading

from django.http import HttpResponse

from traffic_map.service.update_service import run_import


def do_import(request):
    t = threading.Thread(target=run_import)
    t.setDaemon(True)
    t.start()
    return HttpResponse()