from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    organiser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=150)
    sport_type = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    date = models.DateField()
    start_time = models.TimeField()
    capacity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Booking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['event', 'student'],
                name = 'unique_event_booking'
            )
        ]

    def __str__(self):
        return f"{self.student.username} -> {self.event.title}"
# Create your models here.
