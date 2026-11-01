import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

SERVICE = Service(
    executable_path=r'C:\Users\katas\.cache\selenium\chromedriver\win64\156.0.8078.80\chromedriver.exe'
)

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

    print(f'\nstart browser for test.. language={language}')
    browser = webdriver.Chrome(service=SERVICE, options=options)
    yield browser
    print('\nquit browser..')
    browser.quit()