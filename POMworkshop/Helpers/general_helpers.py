from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class Helper:

    def __init__(self, driver, test_logger):
        self.driver = driver
        self.test_logger = test_logger
        self.actions = ActionChains(driver)

    def go_to_page(self, url):
        self.driver.get(url)
        self.test_logger.info(f"Opened URL: {url}")

    def find_elem_ui(self, loc, sec=60):
        try:
            elem = WebDriverWait(self.driver, sec).until(
                EC.visibility_of_element_located(loc))
            return elem
        except Exception as e:
            self.test_logger.error(f"Element not visible: {loc}")
            self.test_logger.error(e)
            raise

    def find_and_click(self, loc, sec=60):
        elem = WebDriverWait(self.driver, sec).until(
            EC.element_to_be_clickable(loc))
        elem.click()

    def find_and_send_keys(self, loc, inp_text, sec=60):
        elem = self.find_elem_ui(loc, sec)
        elem.clear()
        elem.send_keys(inp_text)

    def hover_element(self, loc):
        elem = self.find_elem_ui(loc)
        self.actions.move_to_element(elem).pause(0.5).perform()

    @staticmethod
    def write_in_file(text):
        with open('live_coding.txt', 'a+') as f:
            f.write(text + '\n')
