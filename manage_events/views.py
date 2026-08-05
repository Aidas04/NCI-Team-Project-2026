# Manage Events Views used for backend functionality of the manage events page - Aidas Kibas.

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from datetime import datetime

from home.models import Booking

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
