import allure
import pytest
from allure import severity, severity_level
from axe_selenium_python import Axe
from Common.BaseClass import BaseClass
from Pages.LandingPage import LandingPage


@pytest.mark.parametrize("driver", ["Chrome"], indirect=True)
class TestAccessibility(BaseClass):

    @severity(severity_level.NORMAL)
    @allure.feature('Accessibility')
    @allure.title("Check the landing page accessibility")
    def test_1(self, driver):
        driver.get(BaseClass.url)
        axe = Axe(driver)
        axe.inject()
        results = axe.run()
        if len(results["violations"]) != 0:
            axe_report = axe.report(results["violations"])
            allure.attach(
                axe_report,
                name="Axe Accessibility Report",
                attachment_type=allure.attachment_type.TEXT,
            )
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG
            )
        assert len(results["violations"]) == 0

    @severity(severity_level.NORMAL)
    @allure.feature('Accessibility')
    @allure.title("Check the home page accessibility")
    def test_2(self, driver):
        landing_page_obj = LandingPage(driver)
        landing_page_obj.complete_login(BaseClass.username, BaseClass.password)
        axe = Axe(driver)
        axe.inject()
        results = axe.run()
        if len(results["violations"]) != 0:
            axe_report = axe.report(results["violations"])
            allure.attach(
                axe_report,
                name="Axe Accessibility Report",
                attachment_type=allure.attachment_type.TEXT,
            )
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG
            )
        assert len(results["violations"]) == 0
