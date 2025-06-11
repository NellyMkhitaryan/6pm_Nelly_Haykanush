from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging
import time
import re


class SearchResultsPage:
    # Locators
    RESULT_COUNT_SPAN = (By.CSS_SELECTOR, "span.ns-z")
    PRODUCT_LINKS = (By.CSS_SELECTOR, "a.xR-z")

    brand_filter_button = (By.CSS_SELECTOR, "button[data-test-id-facet-head-name='Brand']")
    color_filter_button = (By.CSS_SELECTOR, "button[data-test-id-facet-head-name='Color']")
    price_filter_button = (By.CSS_SELECTOR, "button[data-test-id-facet-head-name='Price']")
    filter_option_xpath = "//a[@class='it-z']/span[text()='{}']"

    def __init__(self, driver, logger=None):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)
        self.logger = logger or logging.getLogger(__name__)

    def _click_filter(self, filter_button):
        self.wait.until(EC.element_to_be_clickable(filter_button)).click()
        time.sleep(1)

    def _select_filter_value(self, value):
        locator = (By.XPATH, self.filter_option_xpath.format(value))
        try:
            elem = self.wait.until(EC.visibility_of_element_located(locator))
            self.wait.until(EC.element_to_be_clickable(locator))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
            elem.click()
            time.sleep(1)
        except TimeoutException:
            self.logger.warning(f"Filter value '{value}' not found or not clickable")

    def apply_filters(self, brand, color, price):
        self.logger.info(f"Applying filter '{brand}'")
        self._click_filter(self.brand_filter_button)
        self._select_filter_value(brand)

        self.logger.info(f"Applying filter '{color}'")
        self._click_filter(self.color_filter_button)
        self._select_filter_value(color)

        self.logger.info(f"Applying filter '{price}'")
        self._click_filter(self.price_filter_button)
        self._select_filter_value(price)

    def get_result_count_text(self):
        try:
            count_span = self.wait.until(EC.visibility_of_element_located(self.RESULT_COUNT_SPAN))
            count_text = count_span.text.strip()
            self.logger.info(f"Result count text: '{count_text}'")
            return count_text
        except TimeoutException:
            self.logger.error("Result count element not found.")
            return ""

    def get_result_count(self):
        count_text = self.get_result_count_text()
        try:
            count = int(count_text.split()[0])
            return count
        except (ValueError, IndexError):
            self.logger.error(f"Failed to parse result count from text: '{count_text}'")
            return 0

    def check_products_brand_and_price(self, expected_brand, expected_price_max):
        try:
            self.wait.until(EC.presence_of_all_elements_located(self.PRODUCT_LINKS))
            products = self.driver.find_elements(*self.PRODUCT_LINKS)
            if not products:
                self.logger.warning("No product links found.")
                return False

            all_match = True
            for product in products:
                text = product.text.lower()
                self.logger.info(f"Product text: {text}")

                # Check brand presence
                if expected_brand.lower() not in text:
                    self.logger.warning(f"Brand '{expected_brand}' not found in product text.")
                    all_match = False

                # Extract and validate price
                price_match = re.search(r"on sale for \$([\d,.]+)", text)
                if price_match:
                    price_str = price_match.group(1).replace(',', '').strip('.')
                    try:
                        price = float(price_str)
                        if price > expected_price_max:
                            self.logger.warning(
                                f"Product price ${price} exceeds max allowed price ${expected_price_max}."
                            )
                            all_match = False
                    except ValueError:
                        self.logger.warning(f"Could not convert extracted price '{price_str}' to float.")
                        all_match = False
                else:
                    self.logger.warning("Price not found in product description.")
                    all_match = False

            return all_match
        except Exception as e:
            self.logger.error(f"Error validating brand and price: {e}")
            return False
