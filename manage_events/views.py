# Manage Events Views used for backend functionality of the manage events page - Aidas Kibas and Michal Pokojny.

# Imports necessary for the python backend coding of the webpage

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import datetime
from home.models import Event
from .forms import CreateEventForm
from home.models import Booking


# logged in user can change first name and last name, allauth already handles email/password - Michal Pokojny

@login_required(login_url='account_login')
def edit_profile(request):
    user = request.user

    if request.method == "POST":
        user.first_name = request.POST.get("first_name", "").strip()
        user.last_name = request.POST.get("last_name", "").strip()
        user.save(update_fields=["first_name", "last_name"])
        messages.success(request, "Your details have been updated.")
        return redirect("edit_profile")

    return render(request, "manage_events/edit_profile.html", {"user": user})

# organiser create event page, only logged in users can get here
# we also check the password matches before letting them create the event
@login_required(login_url='account_login')
def create_event(request):
    if request.method == "POST":
        form = CreateEventForm(request.POST)
        if form.is_valid():
            # check the password they typed matches their account password
            user = authenticate(
                username=request.user.username,
                password=form.cleaned_data["password"]
            )
            if user is None:
                messages.error(request, "Incorrect password, event not created.")
                return render(request, "manage_events/create_event.html", {"form": form})

            event = form.save(commit=False)
            event.organiser = request.user
            # always basketball for now, user never picks this
            event.sport_type = "Basketball"
            event.save()
            messages.success(request, f"Event '{event.title}' created!")
            return redirect("events")
        else:
            # form not valid, missing fields probably
            messages.error(request, "Please fill in all required fields correctly.")
    else:
        form = CreateEventForm()

    return render(request, "manage_events/create_event.html", {"form": form})

# only the organiser who made the event can delete it
# also needs password again just like create event
@login_required(login_url='account_login')
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # stop randoms deleting events they didnt make
    if event.organiser != request.user:
        messages.error(request, "You can only delete events you organised.")
        return redirect("events")

    if request.method == "POST":
        password = request.POST.get("password")
        user = authenticate(username=request.user.username, password=password)

        if user is None:
            messages.error(request, "Incorrect password, event was not deleted.")
            return redirect("events")

        event_title = event.title
        event.delete()
        messages.success(request, f"Event '{event_title}' deleted.")
        return redirect("events")

    # GET request just shows the confirm page
    return render(request, "manage_events/delete_event.html", {"event": event})

# Aidas Kibas
# Helper function to get user bookings ensuring that the event datetime is timezone-aware and checking if the event is in the past - Aidas Kibas

def get_user_bookings(user):
    bookings = Booking.objects.filter(
        student=user
    ).select_related("event").order_by("-booked_at") # Orders the event based on most recently booked

    # For loop iterating through bookings using the timezone import to create a variable which stores the combined date and start time of an event
    # This tracks the events date and time with the current real date and time for responsive behaviour

    for booking in bookings:
        event_datetime = timezone.make_aware(
            datetime.combine(
                booking.event.date,
                booking.event.start_time
            )
        )

        # Booking.is_past is a variable which determines if a bookings event_datetime is less than the current real time
        # This ensures that booking.is_past can be used to detemine whether an events date and time have passed the current real time

        booking.is_past = event_datetime < timezone.now()

    # Return the bookings 

    return bookings

# Aidas Kibas
# Here i have a function to manage events which checks if the user is authenticated and retrieves their bookings 
# It also checks if the event is in the past and passes the bookings to the template for rendering.

@login_required(login_url='account_login') # Requires login to view the page 
def manage_events(request): # Function name
    bookings = [] # Bookings stored in an array

    # If the user is authenticated, then retreive their bookings by using the get_user_bookings function

    if request.user.is_authenticated:
        bookings = get_user_bookings(request.user)

    # Return the manage_events_page.html to the user

    return render(request, "home/manage_events_page.html", {
        "bookings": bookings,
    })

# Aidas Kibas
# Here i have a function to remove a booking which checks if the user is authenticated and retrieves the booking by its ID. 
# If the booking exists, it deletes it and displays a success message. If the booking does not exist, it displays an error message. 
# Finally, it redirects back to the manage events page.

def remove_booking(request, booking_id):
    if request.user.is_authenticated:
        try:
            booking = Booking.objects.get(id=booking_id, student=request.user)
            booking.delete()
            messages.success(request, "Booking removed successfully.")
        except Booking.DoesNotExist:
            messages.error(request, "Booking not found.")

    return manage_events(request)  # Redirect back to the manage events page

# Aidas Kibas
# Here i have a function to cancel a booking which checks if the user is authenticated and retrieves the booking by its ID.
# If the booking exists, it displays a confirmation message asking the user if they are sure they want to cancel the booking. 
# If the user confirms, it deletes the booking and displays a success message. If the booking does not exist, it displays an error message. 
# Finally, it redirects back to the manage events page.

def cancel_booking(request, booking_id):

    bookings = Booking.objects.filter(id=booking_id, student=request.user)

    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        confirm_refund = request.POST.get("confirm_refund")

        booking = Booking.objects.filter(student=request.user, id=booking_id).first()

        # If confirm cancellation is clicked and the booking exists then delete the booking
        # Display a success message to refund the money (future feature)

        if confirm_refund and booking:
            booking.delete()
            bookings = get_user_bookings(request.user)
            messages.success(request, "You will receive your refund within the next 5 working days.")

        # Else if the confirm cancellation is requested, then display the warning message below 
        # Return the user to the manage_events_page with the booking that is waiting for confirmed cancellation to be clicked

        elif booking:
            messages.warning(
                request,
                f"Are you sure you would like to cancel this event: {booking.event.title}?"
            )
            return render(
                request,
                "home/manage_events_page.html",
                {
                    "bookings": bookings,
                    "pending_booking": booking,
                }
            )

        # Else, display a warning message if the booking does not exist

        else:
            messages.warning(request, "This event does not exist in your booked events.")

        # Return the manage_events_page with current bookings and no pending request bookings

        return render(
        request,
        "home/manage_events_page.html",
        {
            "bookings": bookings,
            "pending_booking": None,
        }
    )
