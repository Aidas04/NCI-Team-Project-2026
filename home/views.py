from django.shortcuts import render
from django.http import HttpResponse
from .models import Event


# Create your views here.
def index(request):
    # Render the home page template
    # return HttpResponse("HOME PAGE OK")
    return render(request, 'home/index.html')

# Events selection page (Nerijus x24170232)
def events(request):
    events = Event.objects.all().order_by("date", "start_time")

    return render(request,
                  "home/events.html",
                  {"events": events})
