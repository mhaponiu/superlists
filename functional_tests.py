from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)#czeka 3s zanim zacznie testy jesli to potrzebne
	
    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        #wchodze glowna strone przegladarki
        self.browser.get('http://localhost:8000')

        #tytul strony i naglowek zawieraja slowo Listy
        self.assertIn('Lista', self.browser.title)
        header_text= self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Listy', header_text)

        #zostaje zachecony do wpisania rzeczy do zrobienia
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Wpisz rzecz do zrobienia'
        )

        #w polu tekstowym wpisuje "kupic pawie piora"
        inputbox.send_keys('Kupić pawie pióra')

        #po nacisnieciu klawisza enter strona zostala uaktualniona i wyswietla
        #"1: Kupić pawie pióra" jako element listy rzeczy do zrobienia.
        inputbox.send_keys(Keys.ENTER)
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Kupić pawie prióra' for row in rows)
        )

        #na stronie dalej jest pole tekstowe do wpisania kolejnego zadania.
        #wpisuję 'Użyć pawich piór do zrobienia przynęty"

        #strona zostala uaktualniona i teraz wyswietla dwa elementy na liscie rzeczy do zrobienia
        self.fail('Zakonczenie testu!')

if __name__ == '__main__':
    unittest.main(warnings='ignore')
