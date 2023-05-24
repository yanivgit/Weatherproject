import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def test_website_is_reachable():
    """
    Test whether the website is reachable by sending
     a GET request to the specified URL.
    """
    url = 'http://127.0.0.1:5000'
    response = requests.get(url)
    assert response.status_code == 200

@pytest.fixture
def web_driver():
    # create a new Chrome session
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(30)
    driver.maximize_window()
    # navigate to the application home page
    driver.get("http://127.0.0.1:5000")
    yield driver
    driver.quit()


def test_valid(web_driver):
    location_input = web_driver.find_element(By.NAME, "location")
    location_input.send_keys("Tel Aviv")

    web_driver.find_element(By.TAG_NAME, "BUTTON").send_keys(Keys.ENTER)

    assert web_driver.find_element(By.NAME, "place").text == "Tel Aviv"


def test_unvalid(web_driver):
    location_input = web_driver.find_element(By.NAME, "location")
    location_input.send_keys("dfjgklfjgfkldn")

    web_driver.find_element(By.TAG_NAME, "BUTTON").send_keys(Keys.ENTER)

    assert web_driver.find_element(By.NAME, "not_found").text == "Couldn't find location, try again"

def test_empty(web_driver):
    location_input = web_driver.find_element(By.NAME, "location")
    location_input.send_keys("")

    web_driver.find_element(By.TAG_NAME, "BUTTON").send_keys(Keys.ENTER)

    assert web_driver.find_element(By.NAME, "not_found").text == "Couldn't find location, try again"


