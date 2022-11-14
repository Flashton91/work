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
    data.pause = 20
    data.name = 'Vasiy'
    data.surname = 'Ivanov'
    data.email = str(randint(1, 1000)) + 'test@test.com'
    data.phone = '9093170' + str(randint(1, 10)) + str(randint(1, 1000)) + str(randint(1, 1000))
    data.comment = 'Тестируем заказ товара'
    return data