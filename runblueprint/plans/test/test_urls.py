from django.test import TestCase
from django.test import Client


class TestUrls(TestCase):
    def setUp(self):
        self.client = Client()  # Every test needs a client.

    # Plan URLS
    def test_plans(self):
        response = self.client.get('/plans/')
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_contact(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)

    # Registration URLs
    def test_login(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_password_reset(self):
        response = self.client.get('/password_reset/')
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 200)
