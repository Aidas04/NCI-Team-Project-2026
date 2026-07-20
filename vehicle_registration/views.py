from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import VehicleRegistrationForm

# Vehicle registration page (Nerijus Kmitas x24170232)
@login_required
def vehicle_registration(request):

    if request.method == "POST":
        form = VehicleRegistrationForm(request.POST)

        if form.is_valid():
            vehicle = form.save(commit=False)

            #Assign logged-in user as  owner of the vehicle
            vehicle.student = request.user

            vehicle.save()

            messages.success(
                request,
                "Vehicle registered successfully!"
            )

            return redirect("vehicle_registration")
        
    else:
        form = VehicleRegistrationForm()

    return render(
            request,
            "vehicle_registration/vehicle_registration.html",
            {
                "form": form
            }
        )
