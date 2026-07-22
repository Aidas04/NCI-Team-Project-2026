#   Edited by:
#   Nerijus Kmitas
#

from django.urls import path
from . import views

urlpatterns = [
    path('', views.vehicle_registration, name='vehicle_registration'),
    path('choice/<int:event_id>/', views.vehicle_choice, name="vehicle_choice"),
]