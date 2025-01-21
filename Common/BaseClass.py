import os
import time

import pytest
import allure
import shutil
import subprocess
from dotenv import load_dotenv
from pytest_check import check
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium import webdriver


def check_with_screenshot(driver, cond, message):
    with check, allure.step(message):
        if not cond:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG
            )
        assert cond


class BaseClass:
    load_dotenv()
    url = os.getenv("URL")
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    browsers = os.getenv("BROWSERS")
    browsers = browsers.split(", ")

    @pytest.fixture(scope="class", autouse=True)
    def driver(self, request):
        print(os.getenv("CURRENT_ENV"))
        browser = request.param

        print(os.getenv('CI'))

        project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if browser == "Edge":
            edge_driver_path = os.path.join(project_folder, 'Resources', 'msedgedriver')
            serv = EdgeService(edge_driver_path)
            driver = webdriver.Edge(service=serv)
        else:
            chrome_driver_path = os.path.join(project_folder, 'Resources', 'chromedriver')
            serv = ChromeService(chrome_driver_path)
            driver = webdriver.Chrome(service=serv)
        driver.implicitly_wait(10)
        driver.maximize_window()
        yield driver
        driver.quit()

    @pytest.fixture(scope="function", autouse=False)
    def proxy_driver(self, request):
        # Set the variables
        browser = request.node.callspec.params["driver"]
        test_name = request.param
        project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        mitmdump_path = shutil.which("mitmdump")
        script_path = os.path.join(project_folder, "Common", "ResponseInterception.py")

        # Check is mitmproxy installed
        if mitmdump_path is None:
            raise FileNotFoundError("mitmdump executable not found in PATH. Please ensure mitmproxy is installed.")

        # Set the proxy port based on the browser
        if browser == "Chrome":
            port = "8082"
        elif browser == "Edge":
            port = "9090"
        else:
            port = "8081"

        # Start the proxy process and check if it started successfully
        mitmdump_process = subprocess.Popen([mitmdump_path, "-s", script_path, "--listen-port", port,
                                             "--set", f"test_name={test_name}"], stdout=subprocess.DEVNULL,
                                            stderr=subprocess.DEVNULL)
        time.sleep(5)
        if mitmdump_process:
            print("Proxy subprocess started")

        # Initiate the driver based on the browser
        if browser == "Edge":
            edge_driver_path = os.path.join(project_folder, 'Resources', 'msedgedriver')
            options = webdriver.EdgeOptions()
            options.add_argument(f'--proxy-server=http://127.0.0.1:{port}')
            options.add_argument('--ignore-certificate-errors')
            serv = EdgeService(edge_driver_path)
            proxy_driver = webdriver.Edge(service=serv, options=options)
        else:
            chrome_driver_path = os.path.join(project_folder, 'Resources', 'chromedriver')
            options = webdriver.ChromeOptions()
            options.add_argument(f'--proxy-server=http://127.0.0.1:{port}')
            options.add_argument('--ignore-certificate-errors')
            serv = ChromeService(chrome_driver_path)
            proxy_driver = webdriver.Chrome(service=serv, options=options)
        proxy_driver.implicitly_wait(10)
        proxy_driver.maximize_window()
        yield proxy_driver
        proxy_driver.quit()

        # Terminate the proxy process and kill it if it doesn't close in 10 seconds
        mitmdump_process.terminate()
        mitmdump_process.wait(timeout=10)
        if mitmdump_process:
            print("Mitmproxy process did not terminate in time. Forcing termination...")
            mitmdump_process.kill()
            time.sleep(5)

    '''@pytest.fixture(scope="session", autouse=True)
    def setup_project_directory(self, request):
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

        # Create Reports/history directory if it doesn't exist
        #os.makedirs(reports_history_path, exist_ok=True)

        # Copy contents of allure-history into Reports/history
        shutil.copytree(allure_history_path, reports_history_path)

        # Teardown: Execute a terminal command at the end of the session
        def generate_report():
            # Replace "your_command" with the terminal command you want to execute
            command = "allure generate ./Reports --clean"
            subprocess.run(command, shell=True, check=True)

        request.addfinalizer(generate_report)'''

