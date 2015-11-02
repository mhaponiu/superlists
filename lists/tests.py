from django.core.urlresolvers import resolve
from django.http.request import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from lists.models import Item, List
from lists.views import home_page


class HomePageTest(TestCase):
    def test_root_url_resolvers_to_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)

        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)

        # @skip('nie wyswietlam juz wszystkich list na stronie glownej')
        # def test_home_page_displays_all_list_items(self):
        #     Item.objects.create(text='itemey 1')
        #     Item.objects.create(text='itemey 2')
        #
        #     request = HttpRequest()
        #     response = home_page(request)
        #
        #     self.assertIn('itemey 1', response.content.decode())
        #     self.assertIn('itemey 1', response.content.decode())


class ListAndItemModelTest(TestCase):
    def test_saving_and_retriving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'Absolutnie pierwszy element listy'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Drugi element'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_item = Item.objects.all()
        self.assertEqual(saved_item.count(), 2)

        first_saved_item = saved_item[0]
        second_saved_item = saved_item[1]
        self.assertEqual(first_saved_item.text, 'Absolutnie pierwszy element listy')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Drugi element')
        self.assertEqual(second_saved_item.list, list_)


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertTemplateUsed(response, 'list.html')

    def test_display_only_items_fot_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='item 1', list=correct_list)
        Item.objects.create(text='item 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='inny element1', list=other_list)
        Item.objects.create(text='inny element2', list=other_list)

        ## client djangowy zamiast selenium (bo test jednostkowy)
        response = self.client.get('/lists/%d/' % (correct_list.id))

        ## Contains zamiast assertIn bo potrafi wyłuskać dane z response
        ##  odrazu bez response.content.decode()
        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')
        self.assertNotContains(response, 'inny element1')
        self.assertNotContains(response, 'inny element2')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)


class NewListTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_file(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        ## zamiast tego:
        ##   request = HttpRequest()
        ##   request.method = 'POST'
        ##   request.POST['item_text'] = 'Nowy element listy'
        ##   response = home_page(request)
        ## client.post
        self.client.post('/lists/%d/add_item' % (correct_list.id,),
                         data={'item_text': 'Nowy element listy'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Nowy element listy')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_after_POST(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.post('/lists/%d/add_item' % (correct_list.id,),
                                    data={'item_text': 'Nowy element listy'})
        ## zamiast recznego sprawdzenia czy przekierowanie nastapilo:
        ## self.assertEqual(response.status_code, 302) 302 - status 'poprawnego przekierowania'
        ## self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
        ## to:
        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))
