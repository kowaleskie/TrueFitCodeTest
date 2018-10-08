import unittest
import json
from selenium import webdriver

browsers = {"windows": {"chrome": r'drivers\windows\chromedriver.exe',
                    "firefox": r'drivers\windows\geckodriver.exe',
                    "edge": r'drivers\windows\MicrosoftWebDriver.exe'},

            "mac": {"chrome": r'drivers/mac/chromedriver',
                    "firefox": r'drivers/mac/geckodriver'},

            "linux": {"chrome": r'drivers/linux/chromedriver',
                      "firefox": r'drivers/linux/geckodriver'}
            }


class TestRunner():
    def __init__(self):

        self.loader = unittest.TestLoader()
        self.suite = self.loader.discover('tests', pattern='*.py')
        self.runner = unittest.TextTestRunner()
        self.runner.run(self.suite)


class MakeDriver():
    """"
    Configures the browser to use from settings in settings.json
    """
    def __init__(self):
        with open('settings.json') as f:
            settings = json.load(f)
        os = settings["os"]


        try:
            if settings['browser'].lower() == "chrome":
                self.driver = webdriver.Chrome(executable_path=browsers[os]["chrome"])
            elif settings['browser'].lower() == "firefox":
                self.driver = webdriver.Firefox(executable_path=browsers[os]["firefox"])
            elif settings['browser'].lower() == "edge":
                self.driver = webdriver.Edge(executable_path=browsers["win"]["edge"])
        except:
            self.driver = webdriver.Chrome(executable_path=browsers["mac"]["chrome"])

        self.driver.set_page_load_timeout(10)
        self.driver.get("http://www.google.com")

    def __del__(self):
        self.driver.close()


if __name__ == '__main__':
    TR = TestRunner()
