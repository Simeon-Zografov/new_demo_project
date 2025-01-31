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
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager


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
    email = os.getenv("EMAIL")
    email_password = os.getenv("EMAIL_PASSWORD")
    browsers = os.getenv("BROWSERS")
    browsers = browsers.split(", ")

    @pytest.fixture(scope="class", autouse=True)
    def driver(self, request):
        browser = request.param
        project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        is_ci = os.getenv('CI') == 'true'
        if is_ci:
            if browser == "Edge":
                # Set up Edge options
                options = EdgeOptions()
                options.add_argument("--headless")
                options.add_argument("--disable-gpu")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-extensions")
                options.add_argument("--disable-infobars")
                serv = EdgeService(EdgeChromiumDriverManager().install())
                driver = webdriver.Edge(service=serv, options=options)
            else:
                options = ChromeOptions()
                options.add_argument("--headless")
                options.add_argument("--disable-gpu")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-extensions")
                options.add_argument("--disable-infobars")
                chrome_driver_path = "/usr/bin/chromedriver"
                serv = ChromeService(chrome_driver_path)
                driver = webdriver.Chrome(service=serv, options=options)
        else:
            if browser == "Edge":
                driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
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

        if os.getenv('CI') == 'true':
            if browser == "Edge":
                options = EdgeOptions()
                options.add_argument("--headless")
                options.add_argument("--disable-gpu")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-extensions")
                options.add_argument("--disable-infobars")
                options.add_argument(f'--proxy-server=https://127.0.0.1:{port}')
                options.add_argument('--ignore-certificate-errors')
                options.add_argument("--allow-insecure-localhost")
                options.add_argument("--disable-http2")
                serv = EdgeService(EdgeChromiumDriverManager().install())
                proxy_driver = webdriver.Edge(service=serv, options=options)
            else:
                options = ChromeOptions()
                options.add_argument("--headless")
                options.add_argument("--disable-gpu")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-extensions")
                options.add_argument("--disable-infobars")
                options.add_argument(f'--proxy-server=http://127.0.0.1:{port}')
                options.add_argument('--ignore-certificate-errors')
                chrome_driver_path = "/usr/bin/chromedriver"
                serv = ChromeService(chrome_driver_path)
                proxy_driver = webdriver.Chrome(service=serv, options=options)
        else:
            # Initiate the driver based on the browser
            if browser == "Edge":
                options = webdriver.EdgeOptions()
                options.add_argument(f'--proxy-server=http://127.0.0.1:{port}')
                options.add_argument('--ignore-certificate-errors')
                proxy_driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()),
                                              options=options)
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
