from traffic_map.ui.views.mapView import map_view_main


def fetch_map(request):
    return map_view_main(request)
