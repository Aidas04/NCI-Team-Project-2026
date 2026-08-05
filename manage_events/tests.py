# Aidas Kibas - Manage Events Page Tests

# Here i import all the necessary modules and classes for testing the manage events page in a Django application.

from django.contrib.auth import get_user_model
from django.http import response
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from home.models import Booking, Event

# Here i create a class called ManageEventsTests that inherits from TestCase. This class contains test methods for the manage events page.

class ManageEventsTests(TestCase):

# Here i create a test user and log them in with test credentials.

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword"
        )

# Here i create a test method called test_authenticated_user_sees_bookings. 
# This method tests that an authenticated user can see their bookings on the manage events page.

    def test_authenticated_user_sees_bookings(self):
        self.client.login(username="testuser", password="testpassword")
        event = Event.objects.create(
            # Test Event details
            organiser=self.user,
            title="Test Event",
            sport_type="Test Sport",
            location="Test Location",
            date="2026-09-15",
            start_time="10:00",
            capacity=10,
            
        )
        booking = Booking.objects.create(
            student=self.user,
            event=event,
        )
        response = self.client.get(reverse("manage_events"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Event")

# Here i create a test method called test_unauthenticated_user_redirected.
# This method tests that an unauthenticated user is redirected to the login page when trying to access the manage events page.

    def test_unauthenticated_user_redirected(self):
        response = self.client.get(reverse("manage_events"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('account_login')}?next={reverse('manage_events')}")

# Here i create a test method called test_remove_booking_removes_booking.
# This method tests that when a user removes a booking, the booking is actually deleted from the usesr's bookings.

    def test_remove_booking_removes_booking(self):
        self.client.login(username="testuser", password="testpassword")
        event = Event.objects.create(
            #Test Event details
            organiser=self.user,
            title="Test Event",
            sport_type="Test Sport",
            location="Test Location",
            date="2026-09-15",
            start_time="10:00",
            capacity=10,
        )
        booking = Booking.objects.create(
            student=self.user,
            event=event,
        )
        response = self.client.post(reverse("remove_booking", args=[booking.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Booking.objects.filter(id=booking.id).exists())
    