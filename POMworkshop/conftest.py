import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import logging
import os
from datetime import datetime
import allure


@pytest.fixture()
def test_driver():
    options = Options()
    options.add_argument("--headless")  # Enable headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture()
def test_logger(request):
    today_date = datetime.today().date()
    log_dir = f"logs_{today_date}"
    os.makedirs(log_dir, exist_ok=True)
    test_name = request.node.name
    log_path = os.path.join(log_dir, f"{test_name}.log")

    logger = logging.getLogger(test_name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_path, mode='w')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.info(f'{test_name} started')
    yield logger
    logger.info(f'{test_name} finished')


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    result = outcome.get_result()
    if result.when == "call" and result.failed:
        driver = item.funcargs.get("test_driver")
        if driver:
            allure.attach(driver.get_screenshot_as_png(),
                          name=f"{item.name}_screenshot",
                          attachment_type=allure.attachment_type.PNG)
