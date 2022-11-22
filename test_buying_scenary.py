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
            ok1 = 'Товар реально в корзине и его цена как в каталоге'
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
        print('ok++++')
        ok2 = 'Цена итоговая и доставка соответствуют финальной цене'

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
        print('ok+++++')
        ok3 = 'Заказ оформлен и цена такая как быа указанна в корзине'
    driver.implicitly_wait(data.pause + 50)

    print(ok1,ok2,ok3)
    assert(ok1 and ok2 and ok3)

def test_promocode(driver, data):
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
        driver.implicitly_wait(data.pause)
        driver.find_element(By.XPATH, "// form[@id ='form_cart1'] // input[@class ='promocode-input']").send_keys(promocode[i])
        driver.implicitly_wait(data.pause)
        driver.find_element(By.ID, "apply_promocode").click()
        driver.implicitly_wait(data.pause)

        driver.implicitly_wait(data.pause)
        itogop = driver.find_element(By.XPATH,"// form[@id ='form_cart1'] // span[@class ='total_price_block'][1] // span[@class ='price']").text
        itogo.append(itogop)

        driver.implicitly_wait(data.pause)
        koplatep = driver.find_element(By.XPATH,"// form[@id ='form_cart1'] // span[@class ='total_price_block'][2] // span[@class ='price']").text
        koplate.append(koplatep)

        driver.implicitly_wait(data.pause)
        dostabkap = (driver.find_element(By.XPATH, "// div[@id ='delivery_price'] // span[@class ='price']")).text
        dostabka.append(dostabkap)

        driver.implicitly_wait(data.pause)
        sdtotalp = (driver.find_element(By.XPATH, "// div[@id ='delivery_total'] // span[@class ='price']")).text
        sdtotal.append(sdtotalp)

        driver.implicitly_wait(data.pause + 100)
        driver.find_element(By.ID, "reset_promocode").click()
        driver.implicitly_wait(data.pause + 50)

        i = i + 1

    print(itogo)
    print(koplate)
    print(dostabka)
    print(sdtotal)


    pass