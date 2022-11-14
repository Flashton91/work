import time
from select import select
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pytest
import re
from selenium.webdriver.support import expected_conditions as EC

def test_standart_buy(driver, data):
    driver.get(data.url + 'categories/volosy?hideOutOfStock=show&sort=price_decrease')
    driver.implicitly_wait(data.pause)
    cena = driver.find_element(By.XPATH, "//form[@class ='variants'][1]//span[@class ='cards__item__price cards__item__price--actual']").text
    chislo = [float(s) for s in re.findall(r'-?\d+\.?\d*', cena)]

    if chislo[0] >= 10000:
        driver.implicitly_wait(data.pause)
        driver.find_element(By.XPATH, "//form[@class ='variants'][1]//input[@value ='Добавить в корзину']").click()
    elif chislo[0] < 10000:
        driver.get(data.url + 'categories/gigiena?hideOutOfStock=show&sort=price_decrease')
        driver.find_element(By.XPATH, "//form[@class ='variants'][1]//input[@value ='Добавить в корзину']").click()
        driver.get(data.url + 'cart')
    else:
        pytest.skip("Добавьте в раздел волос или гигиены что-нибудь дороже 1000 или почините подключение к БД")

    driver.get(data.url + 'cart')
    driver.implicitly_wait(data.pause)
    spis_obl = Select(driver.find_element(By.ID, "Region"))
    spis_obl.select_by_value("000000080")
    driver.implicitly_wait(data.pause)
    spis_city = Select(driver.find_element(By.ID, "City"))
    spis_city.select_by_value("00004")
    driver.implicitly_wait(data.pause)
    driver.find_element(By.ID, "del_pvz").click()
    driver.implicitly_wait(data.pause)
    spis_pvz = Select(driver.find_element(By.ID, "Delivery"))
    spis_pvz.select_by_value("dost19759")
    driver.implicitly_wait(data.pause)
    driver.find_element(By.XPATH, "//*[ contains (text(), 'получении' ) ]").click()
    driver.implicitly_wait(data.pause)

    driver.find_element(By.XPATH, "//div[@id ='fields']//input[@name ='name']").send_keys(data.name)
    driver.find_element(By.XPATH, "//div[@id ='fields']//input[@name ='sename']").send_keys(data.surname)
    driver.find_element(By.XPATH, "//div[@id ='fields']//input[@name ='email']").send_keys(data.email)
    driver.find_element(By.XPATH, "//div[@id ='fields']//input[@name ='phone']").send_keys(data.phone)
    driver.find_element(By.XPATH, "//div[@id ='fields']//textarea[@name ='comment']").send_keys(data.comment)

    driver.implicitly_wait(data.pause)
    driver.find_element(By.ID, "new_order").click()
    WebDriverWait(driver, 150).until(lambda driver: 'заказ' in driver.title)
    driver.implicitly_wait(250)
    log = (driver.find_element(By.XPATH, "//*[ contains (text(), 'Спасибо' ) ]"))
    driver.implicitly_wait(250)

    print(log)

    assert log






