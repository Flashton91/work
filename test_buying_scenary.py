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
import functions
import selector


def test_standart_buy(driver, data):
# Проверяем стандартную покупку - кладём товар в корзину и оформляем заказ

    driver.get(data.url)

    functions.Nonbanner(driver, data)
    functions.Vhod(driver, data)

    chislo, nazvanie, kolstrp = functions.Vkorzinu(driver, data, 'categories/volosy?hideOutOfStock=show&sort=price_decrease', 'y')

    driver.get(data.url + 'cart')
    driver.implicitly_wait(data.pause)

    try:
        driver.implicitly_wait(data.pause)
        spis_obl = Select(driver.find_element(By.XPATH, selector.KorzinaS.poleregion))
        driver.implicitly_wait(data.pause)
        spis_obl.select_by_value("000000080")
        driver.implicitly_wait(data.pause)
        spis_city = Select(driver.find_element(By.XPATH, selector.KorzinaS.polecity))
        driver.implicitly_wait(data.pause)
        spis_city.select_by_value("00004")
        driver.implicitly_wait(data.pause)
        driver.find_element(By.XPATH, selector.KorzinaS.tabpvz).click()
        driver.implicitly_wait(data.pause)
        spis_pvz = Select(driver.find_element(By.XPATH, selector.KorzinaS.poledellvery))
        driver.implicitly_wait(data.pause)
        spis_pvz.select_by_value("dost19759")
        driver.implicitly_wait(data.pause)
        driver.find_element(By.XPATH, selector.KorzinaS.poleoplaty).click()
        driver.implicitly_wait(data.pause)
    except:
        driver.get(data.url + 'cart')
        driver.implicitly_wait(data.pause + 200)
        driver.find_element(By.XPATH, selector.KorzinaS.poleregion).click()
        driver.implicitly_wait(data.pause + 100)
        spis_obl = Select(driver.find_element(By.XPATH, selector.KorzinaS.poleregion))
        driver.implicitly_wait(data.pause + 100)
        spis_obl.select_by_value("000000080")
        driver.implicitly_wait(data.pause + 100)
        driver.find_element(By.XPATH, selector.KorzinaS.polecity).click()
        driver.implicitly_wait(data.pause + 100)
        spis_city = Select(driver.find_element(By.XPATH, selector.KorzinaS.polecity))
        driver.implicitly_wait(data.pause + 100)
        spis_city.select_by_value("00004")
        driver.implicitly_wait(data.pause + 100)
        driver.find_element(By.XPATH, selector.KorzinaS.tabpvz).click()
        driver.implicitly_wait(data.pause + 100)
        driver.find_element(By.XPATH, selector.KorzinaS.poledellvery).click()
        driver.implicitly_wait(data.pause + 100)
        spis_pvz = Select(driver.find_element(By.XPATH, selector.KorzinaS.poledellvery))
        driver.implicitly_wait(data.pause + 100)
        spis_pvz.select_by_value("dost19759")
        driver.implicitly_wait(data.pause + 100)
        driver.find_element(By.XPATH, selector.KorzinaS.poleoplaty).click()
        driver.implicitly_wait(data.pause)

    driver.find_element(By.XPATH, selector.KorzinaS.polephone ).send_keys(data.phone)
    driver.find_element(By.XPATH, selector.KorzinaS.polecomment ).send_keys(data.comment)
    driver.implicitly_wait(data.pause)

    tr = len(driver.find_elements(By.XPATH, selector.KorzinaS.tabletr))
    i=2
    poz = 0
    pchislo = (str('{0:,}'.format(chislo[0]).replace(',', ' '))).rsplit('.', 2)
    res = pchislo[0]
    while i < tr:
        text_pos = (driver.find_element(By.XPATH, f"//form [@id ='form_cart1'] // table[@id ='purchases'] // tr[{str(i)}]")).text
        if (nazvanie in text_pos):

            poz = 1+poz
        i = i + 1

    driver.implicitly_wait(data.pause)
    totalp = driver.find_element(By.XPATH, selector.KorzinaS.totalprice).text
    totalp = totalp.replace(' ', '')
    total = [float(s) for s in re.findall(r'-?\d+\.?\d*', totalp)]
    total = total[0]

    driver.implicitly_wait(data.pause)
    dostabkap = (driver.find_element(By.XPATH, selector.KorzinaS.dostavkaprice)).text
    dostabka = float(dostabkap)

    driver.implicitly_wait(data.pause)
    sdtotalp = (driver.find_element(By.XPATH, selector.KorzinaS.stotalprice)).text
    sdtotal = float(sdtotalp)

    sotvc = 0
    driver.implicitly_wait(data.pause)
    if total + dostabka == sdtotal:
        sotvc = 1

    finalcp = (str('{0:,}'.format(sdtotal).replace(',', ' '))).rsplit('.', 2)
    finalc = finalcp[0]

    driver.find_element(By.XPATH, selector.KorzinaS.buttonzakaza).click()
    driver.implicitly_wait(data.pause + 50)
    driver.find_element(By.XPATH, selector.KorzinaS.closepopup).click()
    driver.implicitly_wait(data.pause + 50)
    WebDriverWait(driver, 150).until(lambda driver: 'заказ' in driver.title)
    driver.implicitly_wait(data.pause + 50)
    spasibo = len(driver.find_elements(By.XPATH, selector.KorzinaS.slovospasibo))
    deneg = len(driver.find_elements(By.XPATH, f"//*[ contains (text(), '{finalc}' ) ]"))

    driver.implicitly_wait(data.pause + 50)
    print(poz)

    assert poz > 0, 'Товар НЕ добавлен в корзину'
    assert sotvc == 1, 'Итоговая цена и цена доставки в сумме НЕ равны финальной цене (внизу страницы)'
    assert spasibo > 0, 'НЕ оформен заказ и НЕ произведен переход на страницу благодарности'

def test_promocode(driver, data):
# Проверяем работу промокодов и правильность вычисленич скидок
    ok2 = [0, 0, 0]
    #Работа промокода - добавляются товары, активируется промо-код и проверяется правильность расчёта цен
    driver.get(data.url)

    functions.Nonbanner(driver, data)

    chislo, nazvanie, kolstrp = functions.Vkorzinu(driver, data, 'sale?sort=sale&hideOutOfStock=show&page=1', 'n')

    st = 1
    shagstr = round(int(kolstrp) / 5)
    while st <= int(kolstrp):
        if st > 1:
            driver.implicitly_wait(data.pause)
            driver.get(data.url + 'sale?sort=sale&hideOutOfStock=show&page=' + str(st) + '')
            driver.implicitly_wait(data.pause)
        driver.find_element(By.XPATH, selector.CatalogS.knopkapokupki).click()
        driver.implicitly_wait(data.pause + 50)
        st = st + shagstr
    driver.get(data.url + 'cart')
    driver.implicitly_wait(data.pause)

    strok = len(driver.find_elements(By.XPATH, selector.KorzinaS.tabletr ))
    # stt = "// form[@id='form_cart1'] // table[@id='purchases'] / tbody / tr"
    s = 1
    skidprocp = []
    cenatovp = []
    oldp = []
    while s <= strok:
        if len(driver.find_elements(By.XPATH, f"// form[@id='form_cart1'] // table[@id='purchases'] / tbody / tr[{str(s)}] / td[@class='price'] // span[@class='red_sale']")) > 0:
            zs = driver.find_element(By.XPATH, f"// form[@id='form_cart1'] // table[@id='purchases'] / tbody / tr[{str(s)}] / td[@class='price'] // span[@class='red_sale']").text
            zs = zs.replace(' ', '')
            zs = zs.replace('-', '')
            zs = zs.replace('%', '')
            skidprocp.append(int(zs))
        if len(driver.find_elements(By.XPATH, f"// form[@id='form_cart1'] // table[@id='purchases'] / tbody / tr[{str(s)}] / td[@class='price'][2]")) > 0:
            zc = driver.find_element(By.XPATH, f"// form[@id='form_cart1'] // table[@id='purchases'] / tbody / tr[{str(s)}] / td[@class='price'][2]").text
            zc = zc.replace(' ', '')
            zc = zc.replace('руб', '')
            cenatovp.append(int(zc))
        if len(driver.find_elements(By.XPATH, f"// form[@id='form_cart1'] // table[@id='purchases'] / tbody / tr[{str(s)}] / td[@class='price'] // span[@class='old_price_cart']")) > 0:
            zo = driver.find_element(By.XPATH, f"// form[@id='form_cart1'] // table[@id='purchases'] / tbody / tr[{str(s)}] / td[@class='price'] // span[@class='old_price_cart']").text
            zo = zo.replace(' ', '')
            zo = zo.replace('руб', '')
            oldp.append(int(zo))

        s = s + 1

    try:
        driver.implicitly_wait(data.pause)
        driver.find_element(By.XPATH, selector.KorzinaS.polepromocode).send_keys(data.promo_ok)
        driver.implicitly_wait(data.pause + 50)
        driver.find_element(By.XPATH, selector.KorzinaS.knopkapromocode).click()
        driver.implicitly_wait(data.pause + 50)
        ok2[1] = 1
        # Промокод успешно активирован
    except:
        driver.implicitly_wait(data.pause + 100)
        driver.find_element(By.ID, "reset_promocode").click()
        driver.implicitly_wait(data.pause + 100)
        driver.find_element(By.XPATH,selector.KorzinaS.polepromocode).click()
        driver.implicitly_wait(data.pause + 100)
        driver.find_element(By.XPATH,selector.KorzinaS.polepromocode).send_keys(data.promo_ok)
        driver.implicitly_wait(data.pause + 100)
        driver.find_element(By.XPATH, selector.KorzinaS.knopkapromocode).click()
        driver.implicitly_wait(data.pause + 100)

    s2 = 1
    cenatovp2 = []
    while s2 <= strok:
        if len(driver.find_elements(By.XPATH, f"// form[@id='form_cart1'] // table[@id='purchases'] / tbody / tr[{str(s2)}] / td[@class='price'][2]")) > 0:
            zc2 = driver.find_element(By.XPATH, f"// form[@id='form_cart1'] // table[@id='purchases'] / tbody / tr[{str(s2)}] / td[@class='price'][2]").text
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
            #Скидки работают правильно

        c = c+1
    try:
        driver.find_element(By.XPATH, selector.KorzinaS.polepromocode).send_keys(data.promo_pros)
        driver.implicitly_wait(data.pause + 50)
        driver.find_element(By.XPATH, selector.KorzinaS.knopkapromocode).click()
    except:
        driver.implicitly_wait(data.pause + 100)
        driver.find_element(By.XPATH, selector.KorzinaS.polepromocode).click()
        driver.implicitly_wait(data.pause + 100)
        driver.find_element(By.XPATH, selector.KorzinaS.polepromocode).send_keys(data.promo_pros)
        driver.implicitly_wait(data.pause + 100)
        driver.find_element(By.XPATH, selector.KorzinaS.knopkapromocode).click()
        driver.implicitly_wait(data.pause + 100)

    driver.get(data.url)

    assert (ok2[1] == 1 and ok2[2] == 1), 'Промокоды НЕ актиаируются, скидки НЕ рассчитываются правильно'

def test_bad_promocode(driver, data):
# Работа промокода - просроченный, использованный, недостаточная сумма

    driver.get(data.url)

    functions.Nonbanner(driver, data)

    chislo, nazvanie, kolstrp = functions.Vkorzinu(driver, data, 'categories/volosy?hideOutOfStock=show&sort=price_decrease', 'y')

    driver.implicitly_wait(data.pause)

    driver.get(data.url + 'cart')
    driver.implicitly_wait(data.pause)

    promocode = [data.promo_lim, data.promo_pros, data.promo_biglim]
    reactionmsg = ['использован', 'закончилось', 'Дополните']
    koplate = []
    sm = 0
    kolmsg = 0
    while sm < len(promocode):
        try:
            driver.implicitly_wait(data.pause)
            driver.find_element(By.XPATH, selector.KorzinaS.sbrospromokida).click()
            driver.implicitly_wait(data.pause)
            driver.find_element(By.XPATH, selector.KorzinaS.polepromocode).send_keys(promocode[sm])
            driver.implicitly_wait(data.pause + 50)
            driver.find_element(By.XPATH, selector.KorzinaS.knopkapromocode).click()
        except:
            driver.implicitly_wait(data.pause + 100)
            driver.find_element(By.XPATH, selector.KorzinaS.sbrospromokida).click()
            driver.implicitly_wait(data.pause + 100)
            driver.find_element(By.XPATH, selector.KorzinaS.polepromocode).click()
            driver.implicitly_wait(data.pause + 100)
            driver.find_element(By.XPATH, selector.KorzinaS.polepromocode).send_keys(promocode[sm])
            driver.implicitly_wait(data.pause + 100)
            driver.find_element(By.XPATH, selector.KorzinaS.knopkapromocode).click()
            driver.implicitly_wait(data.pause + 100)

        driver.implicitly_wait(data.pause + 200)
        koplatep = driver.find_element(By.XPATH, selector.KorzinaS.polekoplate).text
        koplate.append((koplatep))
        driver.implicitly_wait(data.pause + 200)

        if len(driver.find_elements(By.XPATH, "//*[ contains (text(), '" + reactionmsg[sm] + "' ) ]")) > 0:
            kolmsg = kolmsg + 1
        sm = sm + 1

    print(koplate)

    assert kolmsg == 3
    assert koplate[0] == koplate[1] and koplate[1] == koplate[2], 'С неправильным промокодом может быть скидка'
