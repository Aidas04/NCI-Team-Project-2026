from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Event, Booking

# Create your views here. (Home page)
def index(request):
    # Render the home page template
    # return HttpResponse("HOME PAGE OK")
    return render(request, 'home/index.html')

# Events selection page (Nerijus x24170232)
def events(request):
    events = Event.objects.all().order_by("date", "start_time")

    for event in events:
        event.available_places = event.capacity - event.bookings.count()

    return render(
        request,
        "home/events.html",
        {"events": events})

# Book event (Nerijus Kmitas x24170232)
@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Check if event is already fully booked
    if event.bookings.count() >= event.capacity:
        messages.error(
            request,
            "Sorry, this event is fully booked!"
        )
        return redirect("events")
    
    # Prevent duplicate bookings for the same event
    already_booked = Booking.objects.filter(
        event = event,
        student = request.user
    ).exists()

    if already_booked:
        messages.warning(
            request,
            "You have already joined this event!"
        )
        return redirect("events")
    
    # Create booking (Nerijus Kmitas x24170232)
    Booking.objects.create(
        event = event,
        student = request.user
    )
    messages.success(
        request,
        f"You successfully joined {event.title}!"
    )
    return redirect("events")
