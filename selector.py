class CatalogS:
    zakrivalkapopup = "//div[@class ='popmechanic-js-wrapper'] // div[@class ='popmechanic-close']"
    cennik = "//form[@class ='variants'][1]//span[@class ='cards__item__price cards__item__price--actual']"
    nazvanie = "//form[@class ='variants'][1]//a[@class ='column'][2]"
    knopkapokupki = "// div[@class='cards__list variants'][1] // form[@class='variants'][1] // input[@type='submit' and @data-result-text='Добавлено'][1]"

class KorzinaS:
    pass

class VhodS:
    inputemail = "//div[@id ='content']//input[@name ='email']"
    inputpass = "//div[@id ='content']//input[@name ='password']"
    buttonvhod = "//div[@id ='content']//input[@name ='login']"
