from .base_page import BasePage
from .locators import LoginPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage(BasePage):
    def should_be_login_page(self):
        self.should_be_login_url()
        self.should_be_login_form()
        self.should_be_register_form()

    def should_be_login_url(self):
        assert "login" in self.browser.current_url, "Login url is not presented"

    def should_be_login_form(self):
        assert self.is_element_present(*LoginPageLocators.LOGIN_FORM), "Login form is not presented"

    def should_be_register_form(self):
        assert self.is_element_present(*LoginPageLocators.REGISTER_FORM), "Register form is not presented"

    def register_new_user(self, email, password):  
        email_input = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable(LoginPageLocators.REGISTER_EMAIL)
        )
        email_input.send_keys(email)

        password1_input = self.browser.find_element(*LoginPageLocators.REGISTER_PASSWORD1)
        password1_input.send_keys(password)

        password2_input = self.browser.find_element(*LoginPageLocators.REGISTER_PASSWORD2)
        password2_input.send_keys(password)

        submit_button = self.browser.find_element(*LoginPageLocators.REGISTER_SUBMIT)
        submit_button.click()