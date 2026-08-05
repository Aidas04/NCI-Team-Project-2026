# Manage Events Views used for backend functionality of the manage events page - Aidas Kibas.

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


# logged in user can change first name and last name, allauth already handles email/password
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

# Helper function to get user bookings ensuring that the event datetime is timezone-aware and checking if the event is in the past.
def get_user_bookings(user):
    bookings = Booking.objects.filter(
        student=user
    ).select_related("event").order_by("-booked_at")

    for booking in bookings:
        event_datetime = timezone.make_aware(
            datetime.combine(
                booking.event.date,
                booking.event.start_time
            )
        )

        booking.is_past = event_datetime < timezone.now()

    return bookings

# Here i have a function to manage events which checks if the user is authenticated and retrieves their bookings. It also checks if the event is in the past and passes the bookings to the template for rendering.

@login_required(login_url='account_login')
def manage_events(request):
    bookings = []

    if request.user.is_authenticated:
        bookings = get_user_bookings(request.user)

    for booking in bookings:
        event_datetime = datetime.combine(
            booking.event.date,
            booking.event.start_time
        )

        # Make the datetime timezone-aware
        event_datetime = timezone.make_aware(event_datetime)

        booking.is_past = event_datetime < timezone.now()

    return render(request, "home/manage_events_page.html", {
        "bookings": bookings,
    })

# Here i have a function to remove a booking which checks if the user is authenticated and retrieves the booking by its ID. 
# If the booking exists, it deletes it and displays a success message. If the booking does not exist, it displays an error message. Finally, it redirects back to the manage events page.

def remove_booking(request, booking_id):
    if request.user.is_authenticated:
        try:
            booking = Booking.objects.get(id=booking_id, student=request.user)
            booking.delete()
            messages.success(request, "Booking removed successfully.")
        except Booking.DoesNotExist:
            messages.error(request, "Booking not found.")

    return manage_events(request)  # Redirect back to the manage events page

# Here i have a function to cancel a booking which checks if the user is authenticated and retrieves the booking by its ID.
# If the booking exists, it displays a confirmation message asking the user if they are sure they want to cancel the booking. 
# If the user confirms, it deletes the booking and displays a success message. If the booking does not exist, it displays an error message. Finally, it redirects back to the manage events page.

def cancel_booking(request, booking_id):

    bookings = Booking.objects.filter(id=booking_id, student=request.user)

    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        confirm_refund = request.POST.get("confirm_refund")

        booking = Booking.objects.filter(student=request.user, id=booking_id).first()

        if confirm_refund and booking:
            booking.delete()
            bookings = get_user_bookings(request.user)
            messages.success(request, "Your booking has been canceled.")
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
        else:
            messages.warning(request, "This event does not exist in your booked events.")

        return render(
        request,
        "home/manage_events_page.html",
        {
            "bookings": bookings,
            "pending_booking": None,
        }
    )
