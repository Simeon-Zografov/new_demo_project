import allure
import pytest
from allure import severity, severity_level
from Pages.LandingPage import LandingPage
from Common.BaseClass import BaseClass, check_with_screenshot


@pytest.mark.parametrize("driver", BaseClass.browsers, indirect=True)
class TestLandingPage(BaseClass):

    @severity(severity_level.NORMAL)
    @allure.feature('Landing page')
    @allure.title("Login logo is visible")
    def test_1(self, driver):
        landing_page_obj = LandingPage(driver)
        driver.get(BaseClass.url)
        check_with_screenshot(
            driver,
            landing_page_obj.is_login_logo_visible(),
            "The app logo text is correct after login"
        )
