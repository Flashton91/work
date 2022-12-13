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


def test_standart_buy(driver, data):
    ok1 = [0, 0, 0]
    driver.get(data.url)

    try:
        driver.implicitly_wait(data.pause + 50)
        driver.find_element(By.XPATH, "//div[@class ='popmechanic-js-wrapper'] // div[@class ='popmechanic-close']").click()
        driver.implicitly_wait(data.pause)
    except NoSuchElementException:
        driver.get(data.url)
        driver.implicitly_wait(data.pause + 200)
        driver.find_element(By.XPATH, "//div[@class ='popmechanic-js-wrapper'] // div[@class ='popmechanic-close']").click()
        driver.implicitly_wait(data.pause + 200)

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
        driver.find_element(By.XPATH, "// div[@class='cards__list variants'][1] // form[@class='variants'][1] // input[@type='submit' and @data-result-text='Добавлено'][1]").click()
    else:
        pytest.skip("Добавьте в раздел волос что-нибудь дороже 1000 или почините подключение к БД")

    driver.get(data.url + 'cart')
    driver.implicitly_wait(data.pause)

    try:
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
    except:
        driver.get(data.url + 'cart')
        driver.implicitly_wait(data.pause + 200)
        driver.find_element(By.ID, "Region").click()
        driver.implicitly_wait(data.pause + 100)
        spis_obl = Select(driver.find_element(By.ID, "Region"))
        driver.implicitly_wait(data.pause + 100)
        spis_obl.select_by_value("000000080")
        driver.implicitly_wait(data.pause + 100)
        driver.find_element(By.ID, "City").click()
        driver.implicitly_wait(data.pause + 100)
        spis_city = Select(driver.find_element(By.ID, "City"))
        driver.implicitly_wait(data.pause + 100)
        spis_city.select_by_value("00004")
        driver.implicitly_wait(data.pause + 100)
        driver.find_element(By.ID, "del_pvz").click()
        driver.implicitly_wait(data.pause + 100)
        driver.find_element(By.ID, "Delivery").click()
        driver.implicitly_wait(data.pause + 100)
        spis_pvz = Select(driver.find_element(By.ID, "Delivery"))
        driver.implicitly_wait(data.pause + 100)
        spis_pvz.select_by_value("dost19759")
        driver.implicitly_wait(data.pause + 100)
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
    ok2 = [0, 0, 0]
    driver.get(data.url)

    try:
        driver.implicitly_wait(data.pause + 50)
        driver.find_element(By.XPATH,"//div[@class ='popmechanic-js-wrapper'] // div[@class ='popmechanic-close']").click()
        driver.implicitly_wait(data.pause)
    except NoSuchElementException:
        driver.get(data.url)
        driver.implicitly_wait(data.pause + 200)
        driver.find_element(By.XPATH,"//div[@class ='popmechanic-js-wrapper'] // div[@class ='popmechanic-close']").click()
        driver.implicitly_wait(data.pause + 200)

    driver.get(data.url + 'sale?sort=sale&hideOutOfStock=show&page=1')
    try:
        kolstrp = driver.find_element(By.XPATH, "// section[@class ='paginator paginator--top'] // div[@class ='paginator__item'] // div[@class ='pagination'] // a[last()]").text
    except:
        pytest.skip("Добавьте несколько страниц товаров со скидками")
    shagstr = round(int(kolstrp) / 5)
    if int(kolstrp) < 5:
        pytest.skip("Добавьте несколько страниц товаров со скидками")
    st = 1
    while st <= int(kolstrp):
        if st > 1:
            driver.implicitly_wait(data.pause)
            driver.get(data.url + 'sale?sort=sale&hideOutOfStock=show&page=' + str(st) + '')
            driver.implicitly_wait(data.pause)
        driver.find_element(By.XPATH, "// div[@class='cards__list variants'][1] // form[@class='variants'][1] // input[@type='submit' and @data-result-text='Добавлено'][1]").click()
        driver.implicitly_wait(data.pause + 50)
        st = st + shagstr
    driver.get(data.url + 'cart')
    driver.implicitly_wait(data.pause)

    strok = len(driver.find_elements(By.XPATH, "// form[@id='form_cart1'] // table[@id='purchases'] / tbody / tr"))
    s = 1
    skidprocp = []
    cenatovp = []
    oldp = []
    while s <= strok:
        if len(driver.find_elements(By.XPATH, "// form[@id='form_cart1'] // table[@id='purchases'] / tbody / tr[" + str(s) + "] / td[@class='price'] // span[@class='red_sale']")) > 0:
            zs = driver.find_element(By.XPATH, "// form[@id='form_cart1'] // table[@id='purchases'] / tbody / tr[" + str(s) + "] / td[@class='price'] // span[@class='red_sale']").text
            zs = zs.replace(' ', '')
            zs = zs.replace('-', '')
            zs = zs.replace('%', '')
            skidprocp.append(int(zs))
        if len(driver.find_elements(By.XPATH, "// form[@id='form_cart1'] // table[@id='purchases'] / tbody / tr[" + str(s) + "] / td[@class='price'][2]")) > 0:
            zc = driver.find_element(By.XPATH, "// form[@id='form_cart1'] // table[@id='purchases'] / tbody / tr[" + str(s) + "] / td[@class='price'][2]").text
            zc = zc.replace(' ', '')
            zc = zc.replace('руб', '')
            cenatovp.append(int(zc))
        if len(driver.find_elements(By.XPATH, "// form[@id='form_cart1'] // table[@id='purchases'] / tbody / tr[" + str(s) + "] / td[@class='price'] // span[@class='old_price_cart']")) > 0:
            zo = driver.find_element(By.XPATH, "// form[@id='form_cart1'] // table[@id='purchases'] / tbody / tr[" + str(s) + "] / td[@class='price'] // span[@class='old_price_cart']").text
            zo = zo.replace(' ', '')
            zo = zo.replace('руб', '')
            oldp.append(int(zo))

        s = s + 1

    promocode = [data.promo_lim, data.promo_pros, data.promo_ok]
    reactionmsg = ['использован', 'закончилось', 'принят']
    koplate = []
    sm = 0
    kolmsg = 0
    while sm < len(promocode):
        try:
            driver.implicitly_wait(data.pause)
            driver.find_element(By.ID, "reset_promocode").click()
            driver.implicitly_wait(data.pause)
            driver.find_element(By.XPATH, "// div[@class='promocode-input-block'] // input[@class = 'promocode-input']").send_keys(promocode[sm])
            driver.implicitly_wait(data.pause + 50)
            driver.find_element(By.ID, "apply_promocode").click()
        except:
            driver.implicitly_wait(data.pause + 100)
            driver.find_element(By.ID, "reset_promocode").click()
            driver.implicitly_wait(data.pause + 100)
            driver.find_element(By.XPATH, "// div[@class='promocode-input-block'] // input[@class = 'promocode-input']").click()
            driver.implicitly_wait(data.pause + 100)
            driver.find_element(By.XPATH, "// div[@class='promocode-input-block'] // input[@class = 'promocode-input']").send_keys(promocode[sm])
            driver.implicitly_wait(data.pause + 100)
            driver.find_element(By.ID, "apply_promocode").click()
            driver.implicitly_wait(data.pause + 100)

        driver.implicitly_wait(data.pause + 200)
        koplatep = driver.find_element(By.XPATH, "// div[@class='promocode-block'] // span[@class='total_price_block'] [last()] // span[@class='price'] [last()]").text
        koplatep = koplatep.replace(' ', '')
        koplatep = koplatep.replace('р.', '')
        koplate.append(int(koplatep))
        driver.implicitly_wait(data.pause + 200)

        if len(driver.find_elements(By.XPATH, "//*[ contains (text(), '" + reactionmsg[sm] + "' ) ]")) > 0:
            kolmsg = kolmsg + 1
        sm = sm + 1

    print('+++',koplate)

    if koplate[0] == koplate[1] and koplate[2] < koplate[0]:
        print('Итоглвые суммы считаются верно')
        ok2[0] = 1

    if kolmsg == 3:
        print('Сообщения выводятся верно')
        ok2[1] = 1
    print(kolmsg)

    driver.implicitly_wait(data.pause)
    s2 = 1
    cenatovp2 = []
    while s2 <= strok:
        if len(driver.find_elements(By.XPATH, "// form[@id='form_cart1'] // table[@id='purchases'] / tbody / tr[" + str(s2) + "] / td[@class='price'][2]")) > 0:
            zc2 = driver.find_element(By.XPATH, "// form[@id='form_cart1'] // table[@id='purchases'] / tbody / tr[" + str(s2) + "] / td[@class='price'][2]").text
            zc2 = zc2.replace(' ', '')
            zc2 = zc2.replace('руб', '')
            cenatovp2.append(int(zc2))
        s2 = s2 + 1
    driver.implicitly_wait(data.pause)
    if len(skidprocp) != len(cenatovp) and len(cenatovp2) != len(cenatovp):
        pytest.skip("Problem")
    c = 0
    pn = []
    pn2 = []
    while c < len(skidprocp):
        if skidprocp[c] < data.promo_proc and (oldp[c]-oldp[c]/100*data.promo_proc < cenatovp2[c]+2) and ((oldp[c]-oldp[c]/100*data.promo_proc > cenatovp2[c]-2)):
            pn.append(1)
        else:
            pn.append(0)
        if skidprocp[c] >= data.promo_proc and cenatovp[c] == cenatovp2[c]:
            pn2.append(1)
        else:
            pn2.append(0)
        if pn[c] + pn2[c] == 1:
            ok2[2] = 1
            print('Скидки работают правильно')
        c = c+1
    try:
        driver.find_element(By.XPATH, "// div[@class='promocode-input-block'] // input[@class = 'promocode-input']").send_keys(data.promo_pros)
        driver.implicitly_wait(data.pause + 50)
        driver.find_element(By.ID, "apply_promocode").click()
    except:
        driver.implicitly_wait(data.pause + 100)
        driver.find_element(By.XPATH, "// div[@class='promocode-input-block'] // input[@class = 'promocode-input']").click()
        driver.implicitly_wait(data.pause + 100)
        driver.find_element(By.XPATH, "// div[@class='promocode-input-block'] // input[@class = 'promocode-input']").send_keys(data.promo_pros)
        driver.implicitly_wait(data.pause + 100)
        driver.find_element(By.ID, "apply_promocode").click()
        driver.implicitly_wait(data.pause + 100)

    print(skidprocp)
    print(cenatovp)
    print(cenatovp2)
    print(oldp)
    print(pn)
    print(pn2)
    print(ok2)
    driver.get(data.url)

    assert (ok2[0] == 1 and ok2[1] == 1 and ok2[2] == 1)