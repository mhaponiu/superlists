from django.http.request import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from lists.views import home_page
from django.core.urlresolvers import resolve
from lists.models import Item


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

class ItemModelTest(TestCase):

    def test_saving_and_retriving_items(self):
        first_item = Item()
        first_item.text = 'Absolutnie pierwszy element listy'
        first_item.save()

        second_item = Item()
        second_item.text = 'Drugi element'
        second_item.save()

        saved_item = Item.objects.all()
        self.assertEqual(saved_item.count(), 2)

        first_saved_item = saved_item[0]
        second_saved_item = saved_item[1]
        self.assertEqual(first_saved_item.text, 'Absolutnie pierwszy element listy')
        self.assertEqual(second_saved_item.text, 'Drugi element')