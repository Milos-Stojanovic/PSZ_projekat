# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
# Extracted data -> Temporary containers (items) -> Storing in database

import scrapy


class RealEstateItem(scrapy.Item):
    # define the fields for your item here like:

    # price
    cenaNekretnine = scrapy.Field() ##

    # main details
    kvadraturaNekretnine = scrapy.Field() ##
    brojSoba = scrapy.Field() ##
    tipGrejanja = scrapy.Field() ##
    imaParking = scrapy.Field() ##
    ukupnoSpratova = scrapy.Field() # za zgrade, koliko ukupno spratova ima zgrada / za kuce, koliko spratova imaju ##
    spratnost = scrapy.Field() # za zgrade, na kom spratu je stan ##
    uknjizeno = scrapy.Field() ##

    # podaci o nekretnini
    tipNekretnine = scrapy.Field() ##
    tipPonude = scrapy.Field() ##
    godinaIzgradnje = scrapy.Field() ##
    brojKupatila = scrapy.Field() ##

    # dodatna opremljenost
    imaTerasu = scrapy.Field() ##
    imaLadju = scrapy.Field() ##
    imaBalkon = scrapy.Field() ##
    imaPodrum = scrapy.Field() ##
    imaLift = scrapy.Field() # za zgrade ## 

    # sigurnosna oprema
    imaKamera = scrapy.Field() ##
    imaAlarm = scrapy.Field() ##
    imaVideoNadzorInterfon = scrapy.Field() ##

    # tehnicka opremljenost
    imaInternet = scrapy.Field() ##
    imaTelefon = scrapy.Field() ##

    # lokacija
    lokacijaGrad = scrapy.Field() ##
    lokacijaDeoGrada = scrapy.Field() ##

    povrsinaZemljista = scrapy.Field() # za kuce, u arima

    pass
