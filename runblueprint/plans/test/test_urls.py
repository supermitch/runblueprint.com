from django.test import Client, TestCase


class TestUrls(TestCase):
    def setUp(self):
        self.longMessage = True
        self.client = Client()  # Every test needs a client.

    def test_status_codes_200(self):
        urls = [
            '', 'plans/', 'about/', 'contact/', 'login/', 'password_reset/',
            'register/', 'logout/',
        ]
        for url in urls:
            self.assertEqual(self.client.get('/' + url).status_code, 200, msg='for url <{}>'.format(url))
