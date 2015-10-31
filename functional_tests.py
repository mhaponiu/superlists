import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        # self.browser.implicitly_wait(3)#czeka 3s zanim zacznie testy jesli to potrzebne

    def tearDown(self):
        self.browser.quit()
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')

        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # wchodze glowna strone przegladarki
        self.browser.get('http://localhost:8000')

        # tytul strony i naglowek zawieraja slowo Listy
        self.assertIn('Listy', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Twoja lista', header_text)

        # zostaje zachecony do wpisania rzeczy do zrobienia
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Wpisz rzecz do zrobienia'
        )

        # w polu tekstowym wpisuje "kupic pawie piora"
        inputbox.send_keys('Kupić pawie pióra')

        # po nacisnieciu klawisza enter strona zostala uaktualniona i wyswietla
        # "1: Kupić pawie pióra" jako element listy rzeczy do zrobienia.
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: Kupić pawie pióra')

        # na stronie dalej jest pole tekstowe do wpisania kolejnego zadania.
        # wpisuję 'Użyć pawich piór do zrobienia przynęty"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Użyć pawich piór do zrobienia przynęty')
        inputbox.send_keys(Keys.ENTER)

        # strona zostala uaktualniona i teraz wyswietla dwa elementy na liscie rzeczy do zrobienia
        self.check_for_row_in_list_table('1: Kupić pawie pióra')
        self.check_for_row_in_list_table('2: Użyć pawich piór do zrobienia przynęty')
        #self.fail('Zakonczenie testu!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
