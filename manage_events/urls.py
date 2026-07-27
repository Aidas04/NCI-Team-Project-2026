#   Edited by:
#   Aidas Kibas
#

from django.urls import path
from . import views

urlpatterns = [
    path('', views.manage_events, name='manage_events'),
    path('booking/remove/<int:booking_id>/', views.remove_booking, name='remove_booking'),
    path('booking/cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]