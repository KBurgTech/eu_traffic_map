from django.urls import path

from . import views
from .api import import_data, fetch_map
from .ui.views import statusView

urlpatterns = [
    path('', views.index_view, name='index'),
    path('status/', statusView.status_view, name='status'),
    path('load/', import_data.do_import, name='import'),
    path('api/map/', fetch_map.fetch_map, name='fetch_map'),
]
