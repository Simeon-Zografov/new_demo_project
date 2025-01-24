import time
import allure
import pytest
from allure import severity, severity_level
from Common.VisualChack import visual_comparison
from Pages.HomePage import HomePage
from Pages.LandingPage import LandingPage
from Common.BaseClass import BaseClass


@pytest.mark.parametrize("driver", ["Chrome"], indirect=True)
class TestVisual(BaseClass):

    @severity(severity_level.NORMAL)
    @allure.feature('Landing page')
    @allure.title("Visual check of the Landing page")
    def test_1(self, driver):
        driver.get(BaseClass.url)
        visual_comparison(driver, "landing_page", "main")

    @severity(severity_level.NORMAL)
    @allure.feature('Home page')
    @allure.title("Visual check of the Home page")
    def test_2(self, driver):
        landing_page_obj = LandingPage(driver)
        driver.get(BaseClass.url)
        landing_page_obj.complete_login(BaseClass.username, BaseClass.password)
        visual_comparison(driver, "home_page", "main")

    @severity(severity_level.NORMAL)
    @allure.feature('Home page')
    @allure.title("Visual check of the Home page after burger button click")
    def test_3(self, driver):
        home_page_obj = HomePage(driver)
        driver.refresh()
        home_page_obj.click_burger_button()
        time.sleep(1)
        visual_comparison(driver, "home_page", "after_burger_button_click")
        home_page_obj.click_logout_button()

    @severity(severity_level.NORMAL)
    @allure.feature('Home page')
    @allure.title("Visual check of the broken Home page")
    def test_4(self, driver):
        landing_page_obj = LandingPage(driver)
        driver.get(BaseClass.url)
        landing_page_obj.complete_login('visual_user', BaseClass.password)
        visual_comparison(driver, "home_page", "main")

    @severity(severity_level.NORMAL)
    @allure.feature('Home page')
    @allure.title("Visual check of the broken Home page after burger button click")
    def test_5(self, driver):
        home_page_obj = HomePage(driver)
        driver.refresh()
        home_page_obj.click_burger_button()
        time.sleep(1)
        visual_comparison(driver, "home_page", "after_burger_button_click")
