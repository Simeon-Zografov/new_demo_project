import allure
import pytest
from pytest_check import check
from allure import severity, severity_level
from Pages.LandingPage import LandingPage
from Pages.HomePage import HomePage
from Common.BaseClass import BaseClass
from Pages.iFrame import iFramePage


@pytest.mark.parametrize("driver", BaseClass.browsers, indirect=True)
class TestLogin(BaseClass):

    @severity(severity_level.NORMAL)
    @allure.feature('Social Media Links')
    @allure.title('Twitter link')
    def test_1(self, driver):
        landing_page_obj = LandingPage(driver)
        home_page_obj = HomePage(driver)
        driver.get(BaseClass.url)
        landing_page_obj.complete_login(BaseClass.username, BaseClass.password)
        home_page_obj.click_twitter_button()
        with check, allure.step("Check twitter heather tex"):
            driver.switch_to.window(driver.window_handles[1])
            assert home_page_obj.get_twitter_heather_text() == "Sauce Labs"
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    @severity(severity_level.NORMAL)
    @allure.feature('Social Media Links')
    @allure.title('Manually open new tab')
    def test_2(self, driver):
        home_page_obj = HomePage(driver)
        twitter_url = home_page_obj.get_twitter_button_url()
        driver.switch_to.new_window('tab')
        driver.get(twitter_url)
        with check, allure.step("Check twitter heather tex"):
            assert home_page_obj.get_twitter_heather_text() == "Sauce Labs"
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    @severity(severity_level.NORMAL)
    @allure.feature('Social Media Links')
    @allure.title('Navigate to iframe')
    def test_3(self, driver):
        iframe_obj = iFramePage(driver)
        driver.get("https://demo.automationtesting.in/Frames.html")
        driver.switch_to.frame("singleframe")
        with check, allure.step("iFrame heather is visible from within the frame"):
            assert iframe_obj.is_iframe_heather_visible()
        iframe_obj.set_input_field("Text field populated")
        driver.switch_to.default_content()
        with check, allure.step("iFrame heather is visible from within the frame"):
            assert iframe_obj.is_home_button_visible()
