import math
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoAlertPresentException
from .locators import BasePageLocators


class BasePage():
    def __init__(self, browser, url, timeout=20):
        self.browser = browser
        self.url = url
        self.browser.implicitly_wait(timeout)

    def open(self):
        self.browser.get(self.url)

    def go_to_login_page(self):
        link = WebDriverWait(self.browser, 10).until(
        EC.element_to_be_clickable(BasePageLocators.LOGIN_LINK)
    )
        link.click()

    def should_be_login_link(self):
        assert self.is_element_present(*BasePageLocators.LOGIN_LINK), "Login link is not presented"

    def is_element_present(self, how, what):
        try:
            self.browser.find_element(how, what)
        except NoSuchElementException:
            return False
        return True

    def solve_quiz_and_get_code(self):
        try:
            WebDriverWait(self.browser, 3).until(EC.alert_is_present())
            alert = self.browser.switch_to.alert
            
            if "Чему равно" in alert.text:
                x = alert.text.split(" ")[2]
                answer = str(math.log(abs((12 * math.sin(float(x))))))
                alert.send_keys(answer)
                alert.accept()
            else:
                print(f"Неожиданный алерт: {alert.text}")
                alert.accept()
                
        except (TimeoutException, NoAlertPresentException):
            print("Алерта не было, идем дальше")

        try:
            WebDriverWait(self.browser, 2).until(EC.alert_is_present())
            alert = self.browser.switch_to.alert
            print(f"Второй алерт: {alert.text}")
            alert.accept()
        except (TimeoutException, NoAlertPresentException):
            pass        
    def is_disappeared(self, how, what, timeout=4):
        try:
            WebDriverWait(self.browser, timeout, 1, TimeoutException).\
                until_not(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return False
        return True

    def is_not_element_present(self, how, what, timeout=4):
        try:
            WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return True
        return False

    def go_to_basket_page(self):
        basket_link = self.browser.find_element(*BasePageLocators.BASKET_LINK)
        basket_link.click()

    def should_be_authorized_user(self):
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(BasePageLocators.USER_ICON)
        )
        assert self.is_element_present(*BasePageLocators.USER_ICON), "User icon is not presented, probably unauthorised user"

