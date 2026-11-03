import pytest
import time
from selenium.webdriver.common.by import By
from pages.product_page import ProductPage
from pages.basket_page import BasketPage
from pages.login_page import LoginPage

@pytest.fixture(autouse=True)
def clear_basket(browser):
    """Очищает корзину перед каждым тестом, чтобы цена не накапливалась."""
    try:
        browser.get("http://selenium1py.pythonanywhere.com/en-gb/basket/")
        while True:
            remove_buttons = browser.find_elements(By.CSS_SELECTOR, ".basket-items .btn-danger")
            if not remove_buttons:
                break
            remove_buttons[0].click()
            time.sleep(0.5)
    except Exception:
        pass

@pytest.mark.need_review
@pytest.mark.xfail(reason="Bug on the site: success message sometimes doesn't appear")
@pytest.mark.parametrize('link', [
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer0",
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer1",
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer2",
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer3",
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer4",
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer5",
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer6",
    pytest.param(
        "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer7",
        marks=pytest.mark.xfail(reason="Bug in product name")
    ),
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer8",
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer9",
])
def test_guest_can_add_product_to_basket(browser, link):
    page = ProductPage(browser, link)
    page.open()
    product_name = page.get_product_name()
    product_price = page.get_product_price()
    page.add_to_basket()
    page.solve_quiz_and_get_code()
    page.should_be_success_message_with_product_name(product_name)
    page.should_be_basket_price_equal_to_product_price(product_price)


def test_guest_should_not_see_success_message_before_adding_to_basket(browser):
    link = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/"
    page = ProductPage(browser, link)
    page.open()
    page.should_not_be_success_message()


def test_guest_cant_see_success_message_after_adding_product_to_basket(browser):
    link = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/"
    page = ProductPage(browser, link)
    page.open()
    page.add_to_basket()
    page.should_not_be_success_message()


def test_guest_cant_see_success_message(browser):
    link = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/"
    page = ProductPage(browser, link)
    page.open()
    page.should_not_be_success_message()


def test_message_disappeared_after_adding_product_to_basket(browser):
    link = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/"
    page = ProductPage(browser, link)
    page.open()
    page.add_to_basket()
    page.should_disappear_success_message()


@pytest.mark.need_review
def test_guest_cant_see_product_in_basket_opened_from_product_page(browser):
    browser.get("http://selenium1py.pythonanywhere.com/en-gb/basket/")
    try:
        while True:
            remove_buttons = browser.find_elements(By.CSS_SELECTOR, ".basket-items .btn-danger")
            if not remove_buttons:
                break
            remove_buttons[0].click()
            time.sleep(0.5)
    except Exception:
        pass

    link = "http://selenium1py.pythonanywhere.com/en-gb/catalogue/the-city-and-the-stars_95/"
    page = ProductPage(browser, link)
    page.open()
    page.go_to_basket_page()
    basket_page = BasketPage(browser, browser.current_url)
    basket_page.should_be_empty_basket()
    basket_page.should_be_empty_basket_message()


@pytest.mark.login
@pytest.mark.need_review
class TestLoginFromProductPage:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, browser):
        self.link = "http://selenium1py.pythonanywhere.com/en-gb/catalogue/the-city-and-the-stars_95/"
        self.page = ProductPage(browser, self.link)
        self.page.open()
        yield

    def test_guest_should_see_login_link(self, browser):
        self.page.should_be_login_link()

    def test_guest_can_go_to_login_page_from_product_page(self, browser):
        self.page.go_to_login_page()


@pytest.mark.add_to_basket
@pytest.mark.need_review
class TestUserAddToBasketFromProductPage:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, browser):
        link = "http://selenium1py.pythonanywhere.com/en-gb/accounts/login/"
        page = LoginPage(browser, link)
        page.open()
        email = str(time.time()) + "@fakemail.org"
        password = "testpassword123"
        page.register_new_user(email, password)

    def test_user_cant_see_success_message(self, browser):
        link = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/"
        page = ProductPage(browser, link)
        page.open()
        page.should_not_be_success_message()

    @pytest.mark.xfail(reason="Bug on the site: success message sometimes doesn't appear")
    def test_user_can_add_product_to_basket(self, browser):
        link = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/"
        page = ProductPage(browser, link)
        page.open()
        product_name = page.get_product_name()
        product_price = page.get_product_price()
        page.add_to_basket()
        page.solve_quiz_and_get_code()
        page.should_be_success_message_with_product_name(product_name)
        page.should_be_basket_price_equal_to_product_price(product_price)

