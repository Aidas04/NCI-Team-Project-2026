#   Edited by:
#   Aidas Kibas
#

from django.urls import path
from . import views

urlpatterns = [
    path('', views.manage_events, name='manage_events')
]