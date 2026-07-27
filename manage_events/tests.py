from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from home.models import Booking, Event


class ManageEventsViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='student', password='password123')
        self.other_user = get_user_model().objects.create_user(username='other', password='password123')

        self.event = Event.objects.create(
            organiser=self.other_user,
            title='Basketball Session',
            sport_type='Basketball',
            location='Court A',
            date='2026-08-01',
            start_time='18:00:00',
            capacity=10,
        )
        self.booking = Booking.objects.create(event=self.event, student=self.user)
        self.other_booking = Booking.objects.create(event=self.event, student=self.other_user)

    def test_unauthenticated_user_sees_login_message(self):
        response = self.client.get(reverse('manage_events'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You are not logged in.')
        self.assertNotContains(response, 'Basketball Session')

    def test_authenticated_user_sees_their_bookings(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('manage_events'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You are logged in as student.')
        self.assertContains(response, 'Basketball Session')
        self.assertNotContains(response, 'No bookings found.')
