#   Edited by:
#   Nerijus Kmitas
#

from django.urls import path
from . import views

urlpatterns = [
    path('', views.vehicle_registration, name='vehicle_registration')
]