from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)#czeka 3s zanim zacznie testy
	
    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('Lista', self.browser.title)
        self.fail('Zakonczenie testu!')

if __name__ == '__main__':
    unittest.main(warnings='ignore')
