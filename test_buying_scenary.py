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
    ok1 = [0, 0, 0]
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

    driver.implicitly_wait(data.pause)
    spis_obl = Select(driver.find_element(By.ID, "Region"))
    driver.implicitly_wait(data.pause)
    spis_obl.select_by_value("000000080")
    driver.implicitly_wait(data.pause)
    spis_city = Select(driver.find_element(By.ID, "City"))
    driver.implicitly_wait(data.pause)
    spis_city.select_by_value("00004")
    driver.implicitly_wait(data.pause)
    driver.find_element(By.ID, "del_pvz").click()
    driver.implicitly_wait(data.pause)
    spis_pvz = Select(driver.find_element(By.ID, "Delivery"))
    driver.implicitly_wait(data.pause)
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
            print('+ Товар реально в корзине и его цена как в каталог')
            ok1[0] = 1
        i = i + 1

    driver.implicitly_wait(data.pause)
    totalp = driver.find_element(By.XPATH, "//form [@id ='form_cart1'] // div[@class ='promocode'] // div[@class ='main_promocode main_promocode_total'] // span[@class ='total_price_block'][2] // span[@class ='price']").text
    totalp = totalp.replace(' ', '')
    total = [float(s) for s in re.findall(r'-?\d+\.?\d*', totalp)]
    total = total[0]

    driver.implicitly_wait(data.pause)
    dostabkap = (driver.find_element(By.XPATH, "// div[@id ='delivery_price'] // span[@class ='price']")).text
    dostabka = float(dostabkap)

    driver.implicitly_wait(data.pause)
    sdtotalp = (driver.find_element(By.XPATH, "// div[@id ='delivery_total'] // span[@class ='price']")).text
    sdtotal = float(sdtotalp)

    driver.implicitly_wait(data.pause)
    if total + dostabka == sdtotal:
        print('+ Цена итоговая и доставка соответствуют финальной цене')
        ok1[1] = 1

    finalcp = (str('{0:,}'.format(sdtotal).replace(',', ' '))).rsplit('.', 2)
    finalc = finalcp[0]

    driver.find_element(By.ID, "new_order").click()
    driver.implicitly_wait(data.pause + 50)
    driver.find_element(By.XPATH, "// div[@id ='modalQuestionnaire'] // button[@class ='fancybox-button fancybox-close-small']").click()
    driver.implicitly_wait(data.pause + 50)
    WebDriverWait(driver, 150).until(lambda driver: 'заказ' in driver.title)
    driver.implicitly_wait(data.pause + 50)
    spasibo = len(driver.find_elements(By.XPATH, "//*[ contains (text(), 'Спасибо' ) ]"))
    deneg = len(driver.find_elements(By.XPATH, "//*[ contains (text(), '" + finalc + "' ) ]"))
    if spasibo > 0 and deneg > 0:
        print('+ Заказ оформлен и цена такая как быа указанна в корзине')
        ok1[2] = 1
    driver.implicitly_wait(data.pause + 50)

    assert(ok1[0] == 1  and ok1[1] == 1  and ok1[2] == 1)

def test_promocode(driver, data):
    ok2 = [0, 0 , 0]
    driver.get(data.url + 'categories/volosy?hideOutOfStock=show&sort=price_decrease')
    driver.implicitly_wait(data.pause)
    cena = driver.find_element(By.XPATH,"//form[@class ='variants'][1]//span[@class ='cards__item__price cards__item__price--actual']").text
    chislo = [float(s) for s in re.findall(r'-?\d+\.?\d*', cena)]
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

    promocode = [data.promo_ok, data.promo_pros, data.promo_lim]
    message = ['принят', 'закончилось', 'использован']
    itogo = []
    dostabka = []
    koplate = []
    sdtotal = []
    alert = []
    i = 0
    s = 0

    while i < 3:
        driver.implicitly_wait(data.pause + 330)
        driver.implicitly_wait(data.pause + 50)
        driver.find_element(By.XPATH, "// form[@id ='form_cart1'] // input[@class ='promocode-input']").send_keys(promocode[i])
        driver.implicitly_wait(data.pause)
        driver.find_element(By.ID, "apply_promocode").click()
        driver.implicitly_wait(data.pause)

        s = 0
        driver.implicitly_wait(data.pause + 100)
        itogost = driver.find_element(By.XPATH,"// form[@id ='form_cart1'] // span[@class ='total_price_block'][1] // span[@class ='price']").text
        itogostp = itogost.replace(' ', '')
        itogof = [float(s) for s in re.findall(r'-?\d+\.?\d*', itogostp)]
        itogo.append(itogof[0])

        s = 0
        driver.implicitly_wait(data.pause + 50)
        koplatest = driver.find_element(By.XPATH,"// form[@id ='form_cart1'] // span[@class ='total_price_block'][last()] // span[@class ='price']").text
        koplatestp = koplatest.replace(' ', '')
        koplatef = [float(s) for s in re.findall(r'-?\d+\.?\d*', koplatestp)]
        koplate.append(koplatef[0])

        s = 0

        driver.implicitly_wait(data.pause + 50)
        dostabkast = (driver.find_element(By.XPATH, "// div[@id ='delivery_price'] // span[@class ='price']")).text
        dostabkastp = dostabkast.replace(' ', '')
        dostabkaf = float(dostabkastp)
        dostabka.append(dostabkaf)

        driver.implicitly_wait(data.pause + 50)
        sdtotalst = (driver.find_element(By.XPATH, "// div[@id ='delivery_total'] // span[@class ='price']")).text
        sdtotalstp = sdtotalst.replace(' ', '')
        sdtotalf = float(sdtotalstp)
        sdtotal.append(sdtotalf)

        driver.implicitly_wait(data.pause + 50)
        alert.append(len(driver.find_elements(By.XPATH, "//*[ contains (text(), '" + message[i] + "' ) ]")))

        driver.implicitly_wait(data.pause + 100)
        driver.find_element(By.ID, "reset_promocode").click()
        driver.implicitly_wait(data.pause + 50)
        driver.find_element(By.ID, "reset_promocode").click()
        driver.implicitly_wait(data.pause + 50)
        driver.get(data.url + 'cart')

        i = i + 1

    ok4 = 0
    ok5 = 0
    ok6 = 0
    if itogo[0] > koplate[0] and koplate[0] == sdtotal[0] and alert[0] >= 1 and dostabka[0] == 0:
        print('При нормальном промокоде скидка есть, доставка бесплатная, сообщение выводится')
        ok2[0] = 1

    if itogo[1] == koplate[1] and dostabka[1] > 0 and alert[1] >= 1:
        print('Если промокод просроченный, то скидки нетЖ, доставка платная')
        ok2[1] = 1

    if itogo[2] == koplate[2] and dostabka[2] > 0 and alert[2] >= 1:
        print('Если промокод уже активирован, то скидки нет, а доставка платная')
        ok2[2] = 1

    assert (ok2[0] == 1 and ok2[1] == 1  and ok2[2] == 1)