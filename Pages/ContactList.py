from selenium.webdriver.common.by import By


class ContactList:

    def __init__(self, driver):
        self.driver = driver
        self.email_filed = (By.ID, "email")
        self.password_field = (By.ID, "password")
        self.submit_button = (By.ID, "submit")
        self.contacts = (By.XPATH, "//table/tr")

    def set_email_filed(self):
        self.driver.find_element(*self.email_filed).send_keys("simeon.hhl.qa@gmail.com")

    def set_password_filed(self):
        self.driver.find_element(*self.password_field).send_keys("Test#1234")

    def click_submit_button(self):
        self.driver.find_element(*self.submit_button).click()

    def complete_login(self):
        self.set_email_filed()
        self.set_password_filed()
        self.click_submit_button()

    def get_name_by_number(self, num):
        return self.driver.find_element(By.XPATH, f"//table/tr[{num}]/td[2]").text

    def get_number_of_contacts(self):
        elements_list = self.driver.find_elements(*self.contacts)
        return len(elements_list)
