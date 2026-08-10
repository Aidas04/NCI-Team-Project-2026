#   Edited by:
#   Aidas Kibas
#

# Importing necessary items for url paths 

from django.urls import path
from . import views

# These are my url paths for the manage events page, it shows all the possible pages that can be accessed from the manage events page

urlpatterns = [
    path('', views.manage_events, name='manage_events'),
    path('create/', views.create_event, name='create_event'),
    path('delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('profile/', views.edit_profile, name='edit_profile'),
    path('booking/remove/<int:booking_id>/', views.remove_booking, name='remove_booking'),
    path('booking/cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]