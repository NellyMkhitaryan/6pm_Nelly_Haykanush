from selenium.webdriver.common.by import By
from helpers.general_helpers import Helper
import time  # For simple wait

class SearchPage(Helper):
    # Locators for filter category buttons
    BTN_BRAND = (By.XPATH, "//button[@data-selected-facet-group-name='brandNameFacet']")
    BTN_COLOR = (By.XPATH, "//button[@data-selected-facet-group-name='colorFacet']")
    BTN_PRICE = (By.XPATH, "//button[@data-selected-facet-group-name='priceFacet']")

    # Dynamic locators for filter options (text placeholders)
    FILTER_BRAND = (By.XPATH, "//ul[@aria-labelledby='brandNameFacet']//span[text()='%s']")
    FILTER_COLOR = (By.XPATH, "//ul[@aria-labelledby='colorFacet']//span[text()='%s']")
    FILTER_PRICE = (By.XPATH, "//ul[@aria-labelledby='priceFacet']//span[text()='%s']")

    RESULT_COUNT_TEXT = (By.XPATH, "//span[contains(text(),'items found')]")
    PRODUCT_ITEMS = (By.CSS_SELECTOR, "div#products article")

    def apply_filters(self, brand, color, price):
        # Apply brand filter
        self.test_logger.info(f"Applying filter '{brand}'")
        self.find_and_click(self.BTN_BRAND)
        self.find_and_click(self.remake_locator(self.FILTER_BRAND, brand))
        self.wait_for_page_load()

        # Apply color filter
        self.test_logger.info(f"Applying filter '{color}'")
        self.find_and_click(self.BTN_COLOR)
        self.find_and_click(self.remake_locator(self.FILTER_COLOR, color))
        self.wait_for_page_load()

        # Apply price filter
        self.test_logger.info(f"Applying filter '{price}'")
        self.find_and_click(self.BTN_PRICE)
        self.find_and_click(self.remake_locator(self.FILTER_PRICE, price))
        self.wait_for_page_load()

    def wait_for_page_load(self, timeout=3):
        # Simple static wait - replace with smarter wait if available
        time.sleep(timeout)

    def get_result_count_text(self):
        return self.find(self.RESULT_COUNT_TEXT, get_text=True)

    def get_result_count(self):
        text = self.get_result_count_text()
        import re
        match = re.search(r"(\d+)", text)
        if match:
            return int(match.group(1))
        return 0
