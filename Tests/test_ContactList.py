import allure
import pytest
from pytest_check import check
from allure import severity, severity_level
from Pages.ContactList import ContactList
from Common.BaseClass import BaseClass
from Common import APIRequests


@pytest.mark.parametrize("driver", BaseClass.browsers, indirect=True)
class TestContactList(BaseClass):

    @severity(severity_level.NORMAL)
    @allure.feature('Contact List')
    @allure.title("Contact list displays wright names")
    def test_1(self, driver):
        driver.get("https://thinking-tester-contact-list.herokuapp.com/")
        contact_list_obj = ContactList(driver)
        contact_list_obj.complete_login()
        # Use the 'get_contact_list' method to get the names dictionary
        names = APIRequests.get_contact_list()
        # Get the dictionary keys and save them in the 'contact_ids' variable
        contact_ids = list(names.keys())
        # Make the first assert to check the number of contacts from the endpoint and displayed ones
        with check, allure.step("The number of displayed contact matches the BE contacts"):
            assert contact_list_obj.get_number_of_contacts() == len(names.keys())
        # Set an iterator to use when calling the 'get_name_by_number' method
        i = 1
        # Iterate through all contacts
        for contact_id in contact_ids:
            # Get the first and the last name in one string
            full_name = names[contact_id]["first_name"] + " " + names[contact_id]["last_name"]
            # Assert the displayed name is the same
            with check, allure.step(f"The name {full_name} matches the DB"):
                assert contact_list_obj.get_name_by_number(i) == full_name
            # Increase the iterator by one
            i += 1

    @severity(severity_level.NORMAL)
    @allure.feature('Contact List')
    @allure.title("Contact list with 1 contact")
    @pytest.mark.parametrize("proxy_driver", ["contact_page_test_2"], indirect=True)
    def test_2(self, proxy_driver):
        proxy_driver.get("https://thinking-tester-contact-list.herokuapp.com/")
        contact_list_obj = ContactList(proxy_driver)
        contact_list_obj.complete_login()
        with check, allure.step("The number of displayed contact is 0"):
            assert contact_list_obj.get_number_of_contacts() == 0
