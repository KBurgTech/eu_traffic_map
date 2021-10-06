from django.urls import path

from . import views
from .api import import_data

urlpatterns = [
    path('', views.main_view, name='index'),
    path('load/', import_data.do_import, name='import'),
]