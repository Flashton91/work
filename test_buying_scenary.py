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
    driver.get(data.url + 'user/register')
    driver.implicitly_wait(data.pause)
    driver.find_element(By.XPATH, "//div[@id ='content']//input[@name ='email']").send_keys(data.email)
    driver.implicitly_wait(data.pause)
    driver.find_element(By.XPATH, "//div[@id ='content']//input[@name ='password']").send_keys(data.password)
    driver.implicitly_wait(data.pause)
    driver.find_element(By.XPATH, "//div[@id ='content']//input[@name ='login']").click()
    driver.implicitly_wait(data.pause)

    driver.get(data.url + 'categories/volosy?hideOutOfStock=show&sort=price_decrease')
    driver.implicitly_wait(data.pause)
    cena = driver.find_element(By.XPATH,"//form[@class ='variants'][1]//span[@class ='cards__item__price cards__item__price--actual']").text
    chislo = [float(s) for s in re.findall(r'-?\d+\.?\d*', cena)]
    nazvanie = driver.find_element(By.XPATH,"//form[@class ='variants'][1]//a[@class ='column'][2]").text

    if chislo[0] > 1000:
        driver.implicitly_wait(data.pause)
        driver.find_element(By.XPATH, "//form[@class ='variants'][1]//input[@value ='Добавить в корзину']").click()
    else:
        pytest.skip("Добавьте в раздел волос что-нибудь дороже 1000 или почините подключение к БД")

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

    driver.find_element(By.XPATH, "//input[@id ='phone']").send_keys(data.phone)
    driver.find_element(By.XPATH, "//div[@id ='fields']//textarea[@name ='comment']").send_keys(data.comment)
    driver.implicitly_wait(data.pause)

    tr = len(driver.find_elements(By.XPATH, "//form [@id ='form_cart1'] //table[@id ='purchases']//tr"))
    i=2
    pchislo = (str('{0:,}'.format(chislo[0]).replace(',', ' '))).rsplit('.', 2)
    res = pchislo[0]
    while i < tr:
        text_pos = (driver.find_element(By.XPATH, "//form [@id ='form_cart1'] // table[@id ='purchases'] // tr[" + str(i) + "]")).text
        if (nazvanie in text_pos) and res in text_pos:
            print('ok+++')
        i = i + 1

    totalp = driver.find_element(By.XPATH, "//form [@id ='form_cart1'] // div[@class ='promocode'] // div[@class ='main_promocode main_promocode_total'] // span[@class ='total_price_block'][2] // span[@class ='price']").text
    totalp = totalp.replace(' ', '')
    total = [float(s) for s in re.findall(r'-?\d+\.?\d*', totalp)]
    dostabka =



    pass






