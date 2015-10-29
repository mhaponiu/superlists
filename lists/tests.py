from django.http.request import HttpRequest
from django.test import TestCase
from lists.views import home_page
from django.core.urlresolvers import resolve


# Create your tests here.
class SmokeTest(TestCase):

    def test_bad_maths(self):
        self.assertEqual(1+1,2)

class HomePageTest(TestCase):

    def test_root_url_resolvers_to_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_gome_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>Lista rzeczy do zrobienia</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))
