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

    def test_vehicle_registration_success(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("vehicle_registration"),
        {
            "registration_plate": "241-D-12345",
            "make": "Toyota",
            "model": "Corolla",
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Vehicle.objects.count(), 1)

    def test_update_existing_vehicle(self):
        Vehicle.objects.create(
            student=self.user,
            registration_plate="241-D-11111",
            make="Toyota",
            model="Corolla",
        )

        self.client.force_login(self.user)
        self.client.post(
            reverse("vehicle_registration"),
            {
                "registration_plate": "241-D-22222",
                "make": "Honda",
                "model": "Civic",
            }
        )

        vehicle = Vehicle.objects.get(student=self.user)

        self.assertEqual(
            vehicle.registration_plate,
            "241-D-22222"
        )
    def test_invalid_post_does_not_create_vehicle(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("vehicle_registration"),
            {
                "registration_plate": "",
                "make": "",
                "model": "",
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Vehicle.objects.count(), 0)
        