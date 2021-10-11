from django.http import HttpResponse
from django.template import loader

from traffic_map.models import RefreshCycle


def status_view(request):
    template = loader.get_template('StatusPage.html')
    cycles = RefreshCycle.objects.all().order_by('-start_time')
    context = {'cycles': cycles}
    return HttpResponse(template.render(context, request))
