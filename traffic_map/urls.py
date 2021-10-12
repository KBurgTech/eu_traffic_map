from django.urls import path

from . import views
from .api import import_data, fetch_map, data_query
from .ui.views import statusView

urlpatterns = [
    path('', views.index_view, name='index'),
    path('status/', statusView.status_view, name='status'),
    path('load/', import_data.do_import, name='import'),
    path('api/accidents/', data_query.get_accidents, name='get_accidents'),
    path('api/roadworks/', data_query.get_roadworks, name='get_roadworks'),
    path('api/liveitems/', data_query.get_liveitems, name='get_liveitems'),

]
