#   Edited by:
#   Aidas Kibas
#

from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_accounts, name='view_accounts')
]