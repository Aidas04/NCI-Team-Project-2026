from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Vehicle(models.Model):
    #Student who owns the vehicle
    #OneToOneField is used because student's will be able to add only one vehicle not multiple
    student = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="vehicle"
    )

    # Vehicle registration plate
    #Unique tells Django that only particular registration exists only ones in a database
    #there can't be more than one vehicle registered with the same registration plate
    registration_plate = models.CharField(
        max_length=15,
        unique=True
    )

    # Vehicle make
    make = models.CharField(
        max_length=50
    )

    #Vehicle model
    model = models.CharField(
        max_length=50
    )

    # Date vehicle was registered
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.registration_plate} ({self.student.username})"