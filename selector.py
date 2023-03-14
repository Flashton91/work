class CatalogS:
    zakrivalkapopup = "//div[@class ='popmechanic-js-wrapper'] // div[@class ='popmechanic-close']"
    cennik = "//form[@class ='variants'][1]//span[@class ='cards__item__price cards__item__price--actual']"
    nazvanie = "//form[@class ='variants'][1]//a[@class ='column'][2]"
    knopkapokupki = "// div[@class='cards__list variants'][1] // form[@class='variants'][1] // input[@type='submit' and @data-result-text='Добавлено'][1]"

class KorzinaS:
    poleregion = "// *[@id ='Region']"
    polecity = "// *[@id ='City']"
    tabpvz = "// *[@id ='del_pvz']"
    poledellvery = "// *[@id ='Delivery']"
    poleoplaty = "//*[ contains (text(), 'получении' ) ]"

    polephone = "//input[@id ='phone']"
    polecomment = "//div[@id ='fields']//textarea[@name ='comment']"

    tabletr = "//form [@id ='form_cart1'] //table[@id ='purchases']//tr"

    totalprice = "// form[@id ='form_cart1'] // div[@class ='promocode'] // div[@class ='main_promocode main_promocode_total'] // span[@class ='total_price_block'][2] // span[@class ='price']"
    dostavkaprice = "// div[@id ='delivery_price'] // span[@class ='price']"
    stotalprice = "// div[@id ='delivery_total'] // span[@class ='price']"

    buttonzakaza = "// *[@id ='new_order']"

    closepopup = "// div[@id ='modalQuestionnaire'] // button[@class ='fancybox-button fancybox-close-small']"

    slovospasibo = "//*[ contains (text(), 'Спасибо' ) ]"



class VhodS:
    inputemail = "//div[@id ='content']//input[@name ='email']"
    inputpass = "//div[@id ='content']//input[@name ='password']"
    buttonvhod = "//div[@id ='content']//input[@name ='login']"
