from django.test import TestCase
from django.urls import reverse

class HomePageTests(TestCase):
    def test_homepage_loads(self):
        response = self.client.get(reverse("view_accounts"))
        self.assertEqual(response.status_code, 200)