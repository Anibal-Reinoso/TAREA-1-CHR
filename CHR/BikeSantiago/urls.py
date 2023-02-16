from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_stations_data, name='station'),
]