import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException


def pytest_addoption(parser):
    parser.addoption(
        '--language',
        action='store',
        default='en',
        help='Choose language for browser'
    )


@pytest.fixture(scope='function')
def browser(request):
    language = request.config.getoption('language')

    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_experimental_option('prefs', {'intl.accept_languages': language})

    # Пытаемся подключиться к уже открытому Chrome (для локального запуска с VPN)
    try:
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        browser = webdriver.Chrome(options=options)
        print("\nПодключились к открытому Chrome (VPN)")
    except WebDriverException:
        # Если не получилось — открываем новый (для GitHub/рецензентов)
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_experimental_option('prefs', {'intl.accept_languages': language})
        browser = webdriver.Chrome(options=options)
        print("\nОткрыли новый Chrome")

    yield browser
    print('\nquit browser..')
    # browser.quit() # Оставляем закомментированным, чтобы не закрывать ваш браузер с VPN