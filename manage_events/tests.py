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
            sport_type="Basketball",
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
            sport_type="Basketball",
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

# Here i create a test method called test_confirm_cancelation_removes_booking.
# This test ensures that when a user clicks confirm cancelation, the booking is removed from the users list of bookings.

    def test_confirm_cancelation_removes_booking(self):
            self.client.login(username="testuser", password="testpassword")
            event = Event.objects.create(
                #Test Event details
                organiser=self.user,
                title="Test Event",
                sport_type="Basketball",
                location="Test Location",
                date="2026-09-15",
                start_time="10:00",
                capacity=10,
            )
            booking = Booking.objects.create(
                student=self.user,
                event=event,
            )
            response = self.client.post(reverse("cancel_booking", args=[booking.id]))
            self.assertEqual(response.status_code, 200)
            self.assertTrue(Booking.objects.filter(id=booking.id).exists())

# Here i create a test method called test_past_booking_shows_past_event.
# This test ensures that events with a past date appear as past events for a users booking that has passed the date and time of an event.
# This ensures that past events show the remove booking button while upcoming events show request cancelation button.

    def test_past_booking_shows_past_event(self):
        self.client.login(username="testuser", password="testpassword")
        event = Event.objects.create(
            organiser=self.user,
            title="Test Event",
            sport_type="Basketball",
            location="Test Location",
            date="2026-08-01",
            start_time="10:00",
            capacity=10,
        )
        booking = Booking.objects.create(
        student=self.user,
        event=event,
        )

        response = self.client.get(reverse("manage_events"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Past Event")

# Here i create a test method called test_upcoming_booking_shows_upcoming_event. This is the opposite of the past event test.
# This test ensures that events with an upcoming date appear as upcoming events for a users bookings.
# This ensures that past events show the remove booking button while upcoming events show request cancelation button.

    def test_upcoming_booking_shows_upcoming_event(self):
            self.client.login(username="testuser", password="testpassword")
            event = Event.objects.create(
                organiser=self.user,
                title="Test Event",
                sport_type="Basketball",
                location="Test Location",
                date="2026-10-01",
                start_time="10:00",
                capacity=10,
            )
            booking = Booking.objects.create(
            student=self.user,
            event=event,
            )
    
            response = self.client.get(reverse("manage_events"))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Upcoming Event")  

# Here i create a test method called test_user_only_sees_their_own_bookings.
# This test runs two users, self_user or local user and other_user or non-local user.
# I create 2 events; one for self_user and one for other_user.
# When the page loads, if i am self_user, i should only see the booking that is created for me.
# When the page loads, if i am other_user, i should only see the booking that is created for me.
# This prevents users from seeing other users' bookings.

    def test_user_only_sees_their_own_bookings(self):
        self.client.login(username="testuser", password="testpassword")

        other_user = get_user_model().objects.create_user(
            username="otheruser",
            email="otheruser@gmail.com",
            password="testpassword"
        )

        event1 = Event.objects.create(
            organiser=self.user,
            title="My Event",
            sport_type="Basketball",
            location="Test Location",
            date="2026-10-15",
            start_time="10:00",
            capacity=10,
        )

        event2 = Event.objects.create(
            organiser=other_user,
            title="Your Event",
            sport_type="Basketball",
            location="Your Location",
            date="2026-10-20",
            start_time="12:00",
            capacity=10,
        )

        Booking.objects.create(
            student=self.user,
            event=event1,
        )

        Booking.objects.create(
            student=other_user,
            event=event2,
        )

        response = self.client.get(reverse("manage_events"))
        self.assertContains(response, "My Event")
        self.assertNotContains(response, "Other User Event")  