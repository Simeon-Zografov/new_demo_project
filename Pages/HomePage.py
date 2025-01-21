from selenium.webdriver.common.by import By
#from selenium.webdriver.support import wait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class HomePage:

    def __init__(self, driver):
        self.driver = driver
        self.app_logo = (By.XPATH, "//div[@class='app_logo']")
        self.inventory_item_card = (By.XPATH, "//div[@class='inventory_item']")
        self.burger_button = (By.ID, "react-burger-menu-btn")
        self.logout_button = (By.ID, "logout_sidebar_link")
        self.twitter_button = (By.XPATH, "//li[@class='social_twitter']/a")

    def is_app_logo_visible(self):
        return self.driver.find_element(*self.app_logo).is_displayed()

    def get_app_logo_text(self):
        return self.driver.find_element(*self.app_logo).text

    def get_inventory_item_cards_number(self):
        elements_list = self.driver.find_elements(*self.inventory_item_card)
        return len(elements_list)

    def click_burger_button(self):
        self.driver.find_element(*self.burger_button).click()

    def click_logout_button(self):
        self.driver.find_element(*self.logout_button).click()

    def complete_logout(self):
        self.click_burger_button()
        self.click_logout_button()

    def click_twitter_button(self):
        self.driver.find_element(*self.twitter_button).click()

    def get_twitter_heather_text(self):
        wait = WebDriverWait(self.driver, 30)
        twitter_heather = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//h2//span[@class='css-1qaijid r-bcqeeo r-qvutc0 r-poiln3']")))
        return twitter_heather.text

    def get_twitter_button_url(self):
        return self.driver.find_element(*self.twitter_button).get_attribute("href")
