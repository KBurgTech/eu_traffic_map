import datetime

from traffic_map.importer.ger.germany_importer import GermanyImporter
from traffic_map.importer.nl.nl_importer import NetherlandsImporter
from traffic_map.models import RefreshCycle


def run_import():
    if RefreshCycle.objects.filter(finished=False).count() > 0:  # Dont run multiple imports at once
        print("Refresh already running!")
        return
    cycle = RefreshCycle(start_time=datetime.datetime.now(), finished=False)
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
        import_actual(cycle.id)
        cycle.finished = False
        cycle.end_time = datetime.datetime.now()
        cycle.status = -1
        cycle.save()


def import_actual(id):
    ger = GermanyImporter(id)
    ger.load_roadwork()
    ger.load_accidents()
    ger.load_liveitems()

    nl = NetherlandsImporter(id)
    nl.load_accidents()
    nl.load_liveitems()
