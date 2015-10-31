from django.http.request import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from lists.views import home_page
from django.core.urlresolvers import resolve


# Create your tests here.
class MathTest(TestCase):

    def test_bad_maths(self):
        self.assertEqual(1+1,2)

class HomePageTest(TestCase):

    def test_root_url_resolvers_to_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)

        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'Nowy element listy'

        response = home_page(request)

        self.assertIn('Nowy element listy', response.content.decode())