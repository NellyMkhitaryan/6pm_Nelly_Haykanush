from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging


class HomePage:
    SEARCH_INPUT = (By.ID, "searchAll")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "#searchForm button")

    def __init__(self, driver, logger=None):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)
        self.logger = logger or logging.getLogger(__name__)

    def go_to_page(self, url):
        self.driver.get(url)
        self.logger.info(f"Opened URL: {url}")

    def search_product(self, product_name):
        self.logger.info(f"Searching for product: {product_name}")
        search_input = self.wait.until(EC.visibility_of_element_located(self.SEARCH_INPUT))
        search_input.clear()
        search_input.send_keys(product_name)
        self.driver.find_element(*self.SEARCH_BUTTON).click()
