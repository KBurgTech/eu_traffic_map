import datetime

from django.db.models import Max

from traffic_map.importer.ger.germany_importer import GermanyImporter
from traffic_map.importer.nl.nl_importer import NetherlandsImporter
from traffic_map.models import RefreshCycle


def run_import():
    if RefreshCycle.objects.filter(finished=False).count() > 0:  # Dont run multiple imports at once
        print("Refresh already running!")
        return
    cycle = RefreshCycle(start_time=datetime.datetime.now(), finished=False, status=0)
    cycle.start_time = datetime.datetime.now()
    cycle.finished = False
    cycle.save()
    try:
        import_actual(cycle.id)
        cycle.finished = True
        cycle.end_time = datetime.datetime.now()
        cycle.status = 1
        cycle.save()
    except Exception as e:
        cycle.finished = True
        cycle.end_time = datetime.datetime.now()
        cycle.status = -1
        cycle.save()
        print(e)


def import_actual(id):
    ger = GermanyImporter(id)
    ger.load_roadwork()
    ger.load_accidents()
    ger.load_liveitems()

    nl = NetherlandsImporter(id)
    nl.load_accidents()
    nl.load_liveitems()
    nl.load_roadwork()


def get_current_cycle():
    v = RefreshCycle.objects.filter(finished=True, status=1).aggregate(Max('id'))['id__max']
    print(v)
    return v
