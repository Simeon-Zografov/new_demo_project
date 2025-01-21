import allure
import pytest
from pytest_check import check
from allure import severity, severity_level
from Common.BaseClass import BaseClass
from Common import Email


@pytest.mark.parametrize("driver", ["Chrome"], indirect=True)
class TestEmailReader(BaseClass):

    @severity(severity_level.NORMAL)
    @allure.feature('Emails')
    @allure.title("Check the latest notification email subject")
    def test_1(self, driver):
        # # # # # # # # # # # # # # # # # # # # # # # #
        #   Steps that trigger the notification       #
        # # # # # # # # # # # # # # # # # # # # # # # #
        email_subject = Email.get_latest_email_subject()
        assert email_subject == 'Plan closed'
