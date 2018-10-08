import unittest
import time

from runner import MakeDriver
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, \
    ElementNotInteractableException, WebDriverException

browser = MakeDriver()

# Uses ID/name to identify elements as they're more reliable than xpath.
google_elements = {"logo_id": "hplogo",
                   "search_box_name": "q",
                   "search_button_name": "btnK"}


class GoogleTests(unittest.TestCase):
    def __init__(self, methodName='test'):

        super(GoogleTests, self).__init__(methodName)

    def setUp(self):

        browser.driver.get("http://www.google.com")

    def test_google_check_logo(self):

        self.check_exists_by_id(google_elements["logo_id"], "Logo")

    def test_google_search_box(self):

        self.check_exists_by_name(google_elements["search_box_name"], "Search Box")

    def test_google_search_button(self):

        self.check_exists_by_name(google_elements["search_button_name"], "Search Button")

    def test_google_text_field(self):

        current_text = self.send_text("True Fit")
        self.assertEqual("True Fit", current_text)

    def test_google_search_results(self):

        self.send_text("True Fit", search=True)

        # check if google search results are present
        boxes = browser.driver.find_element_by_xpath('//*[@id="nav"]/tbody/tr')
        links = boxes.find_elements_by_css_selector('a')
        results = []

        for link in links:
            results.append(link.get_attribute('href'))
        self.assertGreater(len(results), 0)

    def test_google_search_blank_text_field(self):

        browser.driver.find_element_by_name(google_elements["search_box_name"]).clear()

        # Different browsers produce different exceptions.
        try:
            browser.driver.find_element_by_name(google_elements["search_button_name"]).click()
        except ElementNotVisibleException:
            return
        except ElementNotInteractableException:
            return
        except WebDriverException:
            return
        self.assertTrue(False, "Was able to search blank field")

    def check_exists_by_name(self, element_name, element):
        """"
        :param element_name: The elements name that will be used to identify.
        :parameter element: Element for error reporting.
        """

        try:
            browser.driver.find_element_by_name(element_name)
        except NoSuchElementException:
            self.assertTrue(False, "Google {} does not exist".format(element))

    def check_exists_by_id(self, element_id, element):
        """"
        :param element_id: The elements name that will be used to identify.
        :parameter element: Element for error reporting.
        """

        try:
            browser.driver.find_element_by_id(element_id)
        except NoSuchElementException:
            self.assertTrue(False, "Google {} does not exist".format(element))

    def send_text(self, text, search=False):
        """"
        :param text: Text to type in search bar
        :param search: Condition on if search is entered or not.
        """

        try:
            browser.driver.find_element_by_name(google_elements["search_box_name"]).clear()
            browser.driver.find_element_by_name(google_elements["search_box_name"]).send_keys(text)
            time.sleep(1)
            if search:
                browser.driver.find_element_by_name(google_elements["search_button_name"]).click()
        except ElementNotVisibleException:
                self.assertTrue(False, "Element not interactable")

        return browser.driver.find_element_by_name(google_elements["search_box_name"]).get_attribute('value')


if __name__ == '__main__':
    unittest.main()
