from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import VehicleRegistrationForm
from .models import Vehicle

# Vehicle registration page (Nerijus Kmitas x24170232)
@login_required
def vehicle_registration(request):

    # Get event_id from URL when opening the page
    event_id = request.GET.get("event_id")

    try:
        vehicle = request.user.vehicle
    except Vehicle.DoesNotExist:
        vehicle = None

    if request.method == "POST":


        form = VehicleRegistrationForm(
            request.POST,
            instance=vehicle
        )

        if form.is_valid():
            vehicle = form.save(commit=False)

            #Assign logged-in user as  owner of the vehicle
            vehicle.student = request.user

            vehicle.save()

            messages.success(
                request,
                "Vehicle registered successfully!"
            )

            event_id = request.POST.get("event_id")

            if event_id:
                return redirect(
                    "continue_booking",
                    event_id=event_id
                )
            
            return redirect("events")
        
    # Get request (or invalid form)
    form = VehicleRegistrationForm(instance=vehicle)

    return render(
        request,
        "vehicle_registration/vehicle_registration.html",
        {
            "form": form,
            "event_id": event_id,
        }
    )
        

# Option to register a vehicle
@login_required
def vehicle_choice(request, event_id):
    return render(
        request,
        "vehicle_registration/vehicle_choice.html",
        {
            "event_id": event_id
        }
    )

