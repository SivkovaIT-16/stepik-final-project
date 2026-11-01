from .base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class MainPage(BasePage): 
    def go_to_login_page(self):
        login_link = browser.find_element(By.CSS_SELECTOR, "#login_link")
        login_link.click()