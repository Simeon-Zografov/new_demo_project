from selenium.webdriver.common.by import By


class LandingPage:

    def __init__(self, driver):
        self.driver = driver
        self.login_logo = (By.XPATH, "//div[@class='login_logo']")
        self.username_field = (By.NAME, "user-name")
        self.password_field = (By.NAME, "password")
        self.login_button = (By.ID, "login-button")
        self.error_message = (By.XPATH, "//h3")

    def is_login_logo_visible(self):
        return self.driver.find_element(*self.login_logo).is_displayed()

    def set_username_field(self, username):
        self.driver.find_element(*self.username_field).send_keys(username)

    def set_password_field(self, password):
        self.driver.find_element(*self.password_field).send_keys(password)

    def click_login_button(self):
        self.driver.find_element(*self.login_button).click()

    def complete_login(self, username, password):
        self.set_username_field(username)
        self.set_password_field(password)
        self.click_login_button()

    def is_error_message_visible(self):
        return self.driver.find_element(*self.error_message).is_displayed()
