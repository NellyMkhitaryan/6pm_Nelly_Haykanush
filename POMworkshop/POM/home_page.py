from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from helpers.general_helpers import Helper
import logging


class HomePage(Helper):
    SEARCH_INPUT = (By.XPATH, "//input[@id='searchAll']")
    SEARCH_BUTTON = (By.XPATH, "//*[@id='searchForm']/button")

    def __init__(self, driver, logger=None, timeout=30):
        super().__init__(driver, logger)
        self.timeout = timeout

    def go_to_page(self, url):
        try:
            self.test_logger.info(f"Opening URL: {url}")
            self.driver.get(url)
        except Exception as e:
            self.test_logger.error(f"Failed to open URL {url}: {e}")
            raise

    def search_product(self, product_name):
        try:
            self.test_logger.info(f"Searching for product: {product_name}")
            search_input = self.find(self.SEARCH_INPUT, timeout=self.timeout)
            search_input.clear()
            search_input.send_keys(product_name)
            self.find_and_click(self.SEARCH_BUTTON, timeout=self.timeout)
            self.test_logger.info(f"Clicked search button for product: {product_name}")
        except Exception as e:
            self.test_logger.error(f"Error during product search '{product_name}': {e}")
            raise
