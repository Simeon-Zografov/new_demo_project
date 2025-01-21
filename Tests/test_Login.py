import random
import allure
import pytest
from allure import severity, severity_level
from Pages.LandingPage import LandingPage
from Pages.HomePage import HomePage
from Common.BaseClass import BaseClass, check_with_screenshot


@pytest.mark.parametrize("driver", BaseClass.browsers, indirect=True)
# @pytest.mark.flaky(reruns=1, reruns_delay=1, rerun_except="assert")
class TestLogin(BaseClass):

    @severity(severity_level.NORMAL)
    @allure.feature('Login')
    @allure.title('Unsuccessful login')
    # @pytest.mark.flaky(reruns=5, reruns_delay=1)
    @pytest.mark.parametrize('username,password', [
        ("", BaseClass.password),
        (BaseClass.username, ""),
        (BaseClass.username[:-1], BaseClass.password),
        (BaseClass.username, BaseClass.password[:-1])
    ])
    def test_1(self, driver, username, password):
        landing_page_obj = LandingPage(driver)
        driver.get(BaseClass.url)
        landing_page_obj.set_username_field(username)
        landing_page_obj.set_password_field(password)
        landing_page_obj.click_login_button()
        check_with_screenshot(
            driver,
            landing_page_obj.is_error_message_visible(),
            "Error message is visible"
        )
        driver.refresh()

    @severity(severity_level.CRITICAL)
    @allure.feature('Login')
    @allure.title('Successful login')
    # @pytest.mark.flaky(reruns=5, reruns_delay=1)
    def test_2(self, driver):
        landing_page_obj = LandingPage(driver)
        home_page_obj = HomePage(driver)
        landing_page_obj.complete_login(BaseClass.username, BaseClass.password)

        check_with_screenshot(
            driver,
            home_page_obj.is_app_logo_visible(),
            "The app logo is visible after login"
        )
        actual_text = home_page_obj.get_app_logo_text()
        ran = random.choice([True, False])
        if ran:
            expected_text = "Swag Labs 123"
        else:
            expected_text = "Swag Labs"
        check_with_screenshot(
            driver,
            actual_text == expected_text,
            "The app logo text is correct after login"
        )
        check_with_screenshot(
            driver,
            home_page_obj.get_inventory_item_cards_number() > 0,
            "The items are visible after login"
        )
        home_page_obj.complete_logout()
