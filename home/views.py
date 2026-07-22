from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import stripe
from django.conf import settings
from .models import Event, Booking, Payment

stripe.api_key = settings.STRIPE_SECRET_KEY
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
    
    # If user doesn't have registered vehicle,
    # ask wheater they want to register one.
    if not hasattr(request.user, "vehicle"):
        return redirect(
            "vehicle_choice",
            event_id=event.id
        )
    
    # Create booking (Nerijus Kmitas x24170232)
    # Booking.objects.create(
    #     event = event,
    #     student = request.user
    # )
    # messages.success(
    #     request,
    #     f"You successfully joined {event.title}!"
    # )
    return redirect("create_checkout_session", event_id=event.id)


@login_required
def continue_booking(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # To Prevent duplicate bookings
    if Booking.objects.filter(
        event=event,
        student=request.user
    ).exists():
        
        messages.warning(
            request,
            "You have already joined this event!"
        )

        return redirect("events")
    
    #Check if event is fully booked
    if event.bookings.count() >= event.capacity:

        messages.error(
            request,
            "Sorry, this event is fully booked!"
        )

        return redirect("events")
    
    Booking.objects.create(
        event=event,
        student=request.user
    )

    messages.success(
        request,
        f"You successfully joined {event.title}!"
    )

    return redirect("events")

#checkout session creation
@login_required
def create_checkout_session(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    booking, _ = Booking.objects.get_or_create(event=event, student=request.user)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'eur',
                'product_data': {'name': f"Booking: {event.title}"},
                'unit_amount': 1000,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(f'/payments/success/{booking.id}/'),
        cancel_url=request.build_absolute_uri(f'/payments/cancel/{booking.id}/'),
        metadata={'booking_id': booking.id},
    )

    Payment.objects.update_or_create(
        booking=booking,
        defaults={'stripe_checkout_id': session.id, 'amount': 10.00, 'status': 'pending'}
    )

    return redirect(session.url)

def payment_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.payment.status = 'paid'
    booking.payment.save()
    messages.success(request, f"Payment confirmed for {booking.event.title}!")
    return render(request, "home/payment_success.html", {"booking": booking})


def payment_cancel(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.delete()
    messages.warning(request, "Payment cancelled. Your booking was not confirmed.")
    return render(request, "home/payment_cancel.html")

