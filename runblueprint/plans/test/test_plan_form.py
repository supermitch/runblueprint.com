from django_webtest import WebTest

from django.urls import reverse


class AuthTest(WebTest):

    def test_login(self):
        form = self.app.get(reverse('plans')).form
        response = form.submit().follow()
        self.assertEqual(response.status_code, 200)
