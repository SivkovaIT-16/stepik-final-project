from .base_page import BasePage
from .locators import ProductPageLocators


class ProductPage(BasePage):
    def add_to_basket(self):
        button = self.browser.find_element(*ProductPageLocators.ADD_TO_BASKET_BUTTON)
        button.click()

    def get_product_name(self):
        return self.browser.find_element(*ProductPageLocators.PRODUCT_NAME).text

    def get_product_price(self):
        return self.browser.find_element(*ProductPageLocators.PRODUCT_PRICE).text

    def should_be_success_message_with_product_name(self, expected_product_name):
        success_message = self.browser.find_element(*ProductPageLocators.SUCCESS_MESSAGE).text
        assert success_message == expected_product_name, \
            f"Expected product name '{expected_product_name}', but got '{success_message}'"

    def should_be_basket_price_equal_to_product_price(self, expected_product_price):
        basket_price = self.browser.find_element(*ProductPageLocators.BASKET_PRICE_MESSAGE).text
        print(f"Basket price: '{basket_price}', Expected: '{expected_product_price}'")
        assert basket_price == expected_product_price, \
            f"Expected basket price '{expected_product_price}', but got '{basket_price}'"

    def should_not_be_success_message(self):
        assert self.is_not_element_present(*ProductPageLocators.SUCCESS_MESSAGE), \
            "Success message is presented, but should not be"

    def should_disappear_success_message(self):
        assert self.is_disappeared(*ProductPageLocators.SUCCESS_MESSAGE), \
            "Success message is not disappeared"