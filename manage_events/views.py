from django.contrib import messages

from django.shortcuts import render
from django.utils import timezone
from datetime import datetime

from home.models import Booking


def manage_events(request):
    bookings = []

    if request.user.is_authenticated:
        bookings = Booking.objects.filter(student=request.user).select_related('event').order_by('-booked_at')

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

def remove_booking(request, booking_id):
    if request.user.is_authenticated:
        try:
            booking = Booking.objects.get(id=booking_id, student=request.user)
            booking.delete()
            messages.success(request, "Booking removed successfully.")
        except Booking.DoesNotExist:
            messages.error(request, "Booking not found.")

    return manage_events(request)  # Redirect back to the manage events page


def cancel_booking(request, booking_id):

    bookings = Booking.objects.filter(id=booking_id, student=request.user)

    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        confirm_refund = request.POST.get("confirm_refund")

        booking = Booking.objects.filter(student=request.user, id=booking_id).first()

        if confirm_refund and booking:
            booking.delete()
            bookings = Booking.objects.filter(student=request.user)
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

#    if request.user.is_authenticated:
 #       try:
  #          booking = Booking.objects.get(id=booking_id, student=request.user)
   #         booking.delete()
    #        messages.success(request, "Booking canceled successfully.")
     #   except Booking.DoesNotExist:
      #      messages.error(request, "Booking not found.")

    #return manage_events(request)  # Redirect back to the manage events page