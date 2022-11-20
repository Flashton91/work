from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pytest
from random import randint
import string
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


@pytest.fixture()
def driver(request):
    caps = DesiredCapabilities().FIREFOX
    caps["pageLoadStrategy"] = "normal"
    # caps["pageLoadStrategy"] = "eager"  #  interactive
    # caps["pageLoadStrategy"] = "none"
    # caps["pageLoadStrategy"] = "normal" # complete
    driver = webdriver.Firefox(desired_capabilities=caps, executable_path='./drivers/geckodriver')
    yield driver
    driver.quit()

@pytest.fixture()
def data(request):
    data.url = 'https://professionalhair.a-local.ru/'
    data.pause = 50
    data.email = 'test@test1811.com'
    data.password = 'test1811'
    data.phone = '9093174567'
    data.comment = 'Testing'
    return data