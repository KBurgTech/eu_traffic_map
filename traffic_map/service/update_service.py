import datetime

from traffic_map.importer.ger.germany_importer import GermanyImporter
from traffic_map.models import RefreshCycle


def run_import():
    if RefreshCycle.objects.filter(finished=False).count() > 0:  # Dont run multiple imports at once
        print("Refresh already running!")
        return
    cycle = RefreshCycle(start_time=datetime.datetime.now(), finished=False)
    cycle.start_time = datetime.datetime.now()
    cycle.finished = False
    cycle.save()

    import_actual(cycle.id)

    cycle.finished = True
    cycle.end_time = datetime.datetime.now()
    cycle.save()


def import_actual(id):
    ger = GermanyImporter(id)
    ger.load_roadwork()
