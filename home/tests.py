from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from .models import Event, Booking

User = get_user_model()

#Events page tests unit tests
class EventsPageTests(TestCase):
    def setUp(self):
        self.organiser = User.objects.create_user(
            username="organiser", password="testpass123"
        )
        now = timezone.localtime()

        self.past_event = Event.objects.create(
            organiser=self.organiser,
            title="Past Game",
            sport_type="Basketball",
            location="Old Court",
            date=(now - timedelta(days=1)).date(),
            start_time=now.time(),
            capacity=10,
        )
        self.future_event = Event.objects.create(
            organiser=self.organiser,
            title="Future Game",
            sport_type="Basketball",
            location="New Court",
            date=(now + timedelta(days=1)).date(),
            start_time=now.time(),
            capacity=10,
        )

    def test_past_events_are_not_displayed(self):
        response = self.client.get(reverse("events"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Past Game")

    def test_future_events_are_displayed(self):
        response = self.client.get(reverse("events"))
        self.assertContains(response, "Future Game")


class BookEventTests(TestCase):
    def setUp(self):
        self.organiser = User.objects.create_user(
            username="organiser", password="testpass123"
        )
        self.user = User.objects.create_user(
            username="player", password="testpass123"
        )
        now = timezone.localtime()
        self.event = Event.objects.create(
            organiser=self.organiser,
            title="Test Game",
            sport_type="Basketball",
            location="Court A",
            date=(now + timedelta(days=1)).date(),
            start_time=now.time(),
            capacity=1,
        )

    def test_redirects_to_login_if_not_authenticated(self):
        response = self.client.post(reverse("book_event", args=[self.event.id]))
        self.assertEqual(response.status_code, 302)

    def test_blocks_booking_when_event_full(self):
        Booking.objects.create(event=self.event, student=self.organiser)
        self.client.login(username="player", password="testpass123")
        response = self.client.post(
            reverse("book_event", args=[self.event.id]), follow=True
        )
        self.assertContains(response, "fully booked")


class HomePageTests(TestCase):
    def test_homepage_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)