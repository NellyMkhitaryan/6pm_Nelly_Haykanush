from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Helper:
    def __init__(self, driver, test_logger):
        self.driver = driver
        self.test_logger = test_logger
        self.actions = ActionChains(driver)

    def go_to_page(self, url):
        self.test_logger.info(f"Navigate to {url}")
        self.driver.get(url)
        self.driver.maximize_window()

    def find_and_click(self, loc, timeout=30):
        elem = self.find(loc, timeout)
        elem.click()
        # self.test_logger.info(f"Clicked element: {loc}")

    def find_and_send_keys(self, loc, inp_text, timeout=10):
        elem = self.find(loc, timeout)
        elem.clear()
        elem.send_keys(inp_text)
        self.test_logger.info(f"Sent keys '{inp_text}' to element: {loc}")

    def find(self, loc, timeout=20, should_exist=True, get_text=False, get_attribute=""):
        try:
            elem = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(loc),
                message=f"Element '{loc}' not found!"
            )
        except Exception as e:
            self.test_logger.error(f"Error finding element {loc}: {e}")
            if should_exist:
                raise
            return False

        if get_text:
            text = elem.text
            # self.test_logger.info(f"Element text for {loc}: {text}")
            return text
        elif get_attribute:
            attr = elem.get_attribute(get_attribute)
            self.test_logger.info(f"Element attribute '{get_attribute}' for {loc}: {attr}")
            return attr
        return elem

    def find_all(self, loc, timeout=10):
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(loc),
                message=f"Elements '{loc}' not found!"
            )
            self.test_logger.info(f"Found {len(elements)} elements for locator: {loc}")
            return elements
        except Exception as e:
            self.test_logger.error(f"Error finding elements {loc}: {e}")
            return False

    def wait_element_disappear(self, loc, timeout=10):
        self.test_logger.info(f"Waiting for element to disappear: {loc}")
        WebDriverWait(self.driver, timeout).until_not(EC.presence_of_element_located(loc))

    def wait_element_clickable(self, loc, timeout=30):
        self.test_logger.info(f"Waiting for element to be clickable: {loc}")
        WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(loc))

    def wait_for_page(self, page="", not_page="", timeout=10):
        if page:
            self.test_logger.info(f"Waiting for URL to contain: {page}")
            WebDriverWait(self.driver, timeout).until(EC.url_contains(page))
        elif not_page:
            self.test_logger.info(f"Waiting for URL to NOT contain: {not_page}")
            WebDriverWait(self.driver, timeout).until_not(EC.url_contains(not_page))

    def hover_element(self, loc):
        self.test_logger.info(f"Hovering over element: {loc}")
        hover = self.actions.move_to_element(self.find(loc)).pause(0.5)
        hover.perform()

    def wait_for_page_load(self, timeout=30):
        self.test_logger.info(f"Setting page load timeout to {timeout} seconds")
        self.driver.set_page_load_timeout(timeout)

    def remake_locator(self, base_locator, *args):
        locator_type = base_locator[0]
        locator_value = base_locator[1] % args
        # self.test_logger.info(f"Remade locator: ({locator_type}, {locator_value})")
        return locator_type, locator_value
