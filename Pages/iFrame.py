from selenium.webdriver.common.by import By
# from selenium.webdriver.support import wait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class iFramePage:

    def __init__(self, driver):
        self.driver = driver
        self.iframe_heather = (By.XPATH, "//h5")
        self.home_button = (By.XPATH, "//a[.='Home']")
        self.input_field = (By.XPATH, "//input")

    def is_iframe_heather_visible(self):
        return self.driver.find_element(*self.iframe_heather).is_displayed()

    def is_home_button_visible(self):
        return self.driver.find_element(*self.home_button).is_displayed()

    def set_input_field(self, text):
        self.driver.find_element(*self.input_field).send_keys(text)
