import os
import shutil
import subprocess
import pytest


@pytest.fixture(scope="session", autouse=True)
def setup_reporting_directories(request):
    # Setup all needed paths
    project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    reports_path = os.path.join(project_folder, 'Reports')
    reports_history_path = os.path.join(reports_path, 'history')
    allure_history_path = os.path.join(project_folder, 'allure-report', 'history')

    # Clear the content of the Reports directory
    for item in os.listdir(reports_path):
        item_path = os.path.join(reports_path, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

    # Copy contents of allure-history into Reports/history
    if os.path.exists(allure_history_path):
        shutil.copytree(allure_history_path, reports_history_path)


def pytest_sessionfinish():
    # Generate the Allure report after all tests have completed
    project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    reports_path = os.path.join(project_folder, 'Reports')
    command = f"allure generate {reports_path} --clean"
    subprocess.run(command, shell=True, check=True)
