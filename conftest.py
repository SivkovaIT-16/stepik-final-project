import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_experimental_option('prefs', {'intl.accept_languages': language})

    print(f'\nstart browser for test.. language={language}')
    browser = webdriver.Chrome(options=options)
    yield browser
    print('\nquit browser..')
    # browser.quit()

