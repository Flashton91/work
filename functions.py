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
from selenium.common.exceptions import NoSuchElementException
import selector


def Nonbanner(driver, data):
    try:
        driver.implicitly_wait(data.pause + 50)
        driver.find_element(By.XPATH, selector.CatalogS.zakrivalkapopup).click()
        driver.implicitly_wait(data.pause)
    except NoSuchElementException:
        driver.get(data.url)
        driver.implicitly_wait(data.pause + 200)
        driver.find_element(By.XPATH, selector.CatalogS.zakrivalkapopup).click()
        driver.implicitly_wait(data.pause + 200)
    return driver


def Vkorzinu(driver, data, razdel, pricestop):
    driver.get(data.url + razdel)
    kolstrp = driver.find_element(By.XPATH, "// section[@class ='paginator paginator--top'] // div[@class ='paginator__item'] // div[@class ='pagination'] // a[last()]").text
    driver.implicitly_wait(data.pause)
    cena = driver.find_element(By.XPATH, selector.CatalogS.cennik).text
    chislo = [float(s) for s in re.findall(r'-?\d+\.?\d*', cena)]
    nazvanie = driver.find_element(By.XPATH, selector.CatalogS.nazvanie ).text

    if pricestop == 'y':
        if chislo[0] > 1000:
            driver.implicitly_wait(data.pause)
            driver.find_element(By.XPATH, selector.CatalogS.knopkapokupki).click()
        else:
            print('- Добавьте в раздел волос что-нибудь дороже 1000 или почините подключение к БД', file=log)
            pytest.skip("Добавьте в раздел волос что-нибудь дороже 1000 или почините подключение к БД")
    return chislo, nazvanie, kolstrp

def Vhod(driver, data):
    driver.get(data.url + 'user/register')
    driver.implicitly_wait(data.pause)
    driver.find_element(By.XPATH, selector.VhodS.inputemail).send_keys(data.email)
    driver.implicitly_wait(data.pause)
    driver.find_element(By.XPATH, selector.VhodS.inputpass).send_keys(data.password)
    driver.implicitly_wait(data.pause)
    driver.find_element(By.XPATH, selector.VhodS.buttonvhod).click()
    driver.implicitly_wait(data.pause)