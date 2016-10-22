from django.test import Client, TestCase
from django.core.urlresolvers import get_resolver, reverse

from plans import urls as plan_urls


class TestUrls(TestCase):
    def setUp(self):
        self.longMessage = True
        self.client = Client()  # Every test needs a client.


    def test_status_codes_200(self):
        for name in get_resolver(plan_urls).reverse_dict:  # Get all urls for this app
            if type(name) == str:
                url = reverse(name)
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200, msg='URL <{}>'.format(url))
