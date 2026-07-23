from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Vehicle
from .forms import VehicleRegistrationForm

User = get_user_model()


class VehicleModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_vehicle_creation(self):
        vehicle = Vehicle.objects.create(
            student=self.user,
            registration_plate="12D12345",
            make="Toyota",
            model="Corolla",
        )
        self.assertEqual(vehicle.student, self.user)
        self.assertEqual(vehicle.registration_plate, "12D12345")


class VehicleRegistrationFormTests(TestCase):
    def test_valid_form(self):
        form = VehicleRegistrationForm(data={
            "registration_plate": "12D12345",
            "make": "Toyota",
            "model": "Corolla",
        })
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_fields(self):
        form = VehicleRegistrationForm(data={})
        self.assertFalse(form.is_valid())


class VehicleRegistrationViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="test123"
        )

    def test_redirects_if_not_logged_in(self):
        response = self.client.get(reverse("vehicle_registration"))
        self.assertEqual(response.status_code, 302)

    def test_loads_for_logged_in_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("vehicle_registration"))
        self.assertEqual(response.status_code, 200)