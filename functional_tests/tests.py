import unittest

from django.test.testcases import LiveServerTestCase  # dzieki niej django automatycznie tworzy baze testowa
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)  # czeka 3s zanim zacznie testy jesli to potrzebne

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')

        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edyta wchodzi na glowna strone przegladarki
        ## live_server_url to aktualny url+port testowanej strony (django zapewnia)
        self.browser.get(self.live_server_url)

        # tytul strony i naglowek zawieraja slowo Listy
        self.assertIn('Listy', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Utwórz nową listę rzeczy do zrobienia', header_text)

        # zostaje zachecony do wpisania rzeczy do zrobienia
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Wpisz rzecz do zrobienia'
        )

        # w polu tekstowym Edyta wpisuje "kupic pawie piora"
        inputbox.send_keys('Kupić pawie pióra')

        # po nacisnieciu klawisza enter strona zostala uaktualniona i wyswietla
        # "1: Kupić pawie pióra" jako element listy rzeczy do zrobienia.
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: Kupić pawie pióra')

        # Edyta otrzymuje unikalny link do listy
        edyta_list_url = self.browser.current_url
        self.assertRegex(edyta_list_url, '/lists/.+')

        # na stronie dalej jest pole tekstowe do wpisania kolejnego zadania.
        # wpisuję 'Użyć pawich piór do zrobienia przynęty"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Użyć pawich piór do zrobienia przynęty')
        inputbox.send_keys(Keys.ENTER)

        # strona zostala uaktualniona i teraz wyswietla dwa elementy na liscie rzeczy do zrobienia
        self.check_for_row_in_list_table('1: Kupić pawie pióra')
        self.check_for_row_in_list_table('2: Użyć pawich piór do zrobienia przynęty')

        # przychodzi nowy użytkownik Franek
        ## uzywamy nowej sesji przegladarki internetowej, aby miec pewnosc, że żadne
        ## dane dotyczace poprzedniej sesji nie zostana ujawnione np przez cookies
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Franek odwiedza strone glowna
        # nie znajduje zadnych sladow poprzedniej sesji
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_elements_by_tag_name('body')
        self.assertNotIn('Kupić pawie pióra', page_text)
        self.assertNotIn('zrobienia przynęty', page_text)

        # Franek tworzy nową listę, wprowadzając nowy element
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Kupić mleko')
        inputbox.send_keys(Keys.ENTER)

        # Franek otrzymuje unikatowy adres URL prowadzacy do listy
        # adres inny od adresu otrzymanego przez Edyte
        franek_list_url = self.browser.current_url
        self.assertRegex(franek_list_url, '/lists/.+')
        self.assertNotEqual(franek_list_url, edyta_list_url)

        # tylko lista Franka jest, bez danych Edyty
        page_text = self.browser.find_elements_by_tag_name('body').text
        self.assertNotIn('Kupić pawie pióra', page_text)
        self.assertIn('Kupić mleko', page_text)

