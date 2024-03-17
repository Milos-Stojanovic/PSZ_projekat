import scrapy
from ..items import RealEstateItem

class RealEstateSpider(scrapy.Spider): 
    name = 'realEstate'
    #allowed_domains = ['nekretnine.rs']
    start_urls = [  #urls to scrape 
        'https://www.nekretnine.rs/stambeni-objekti/stanovi/izdavanje-prodaja/prodaja/cena/1_100000/lista/po-stranici/20/',
        'https://www.nekretnine.rs/stambeni-objekti/stanovi/izdavanje-prodaja/prodaja/cena/100001_160000/lista/po-stranici/20/',
        'https://www.nekretnine.rs/stambeni-objekti/stanovi/izdavanje-prodaja/prodaja/cena/160001_10000000/lista/po-stranici/20/',
        'https://www.nekretnine.rs/stambeni-objekti/stanovi/izdavanje-prodaja/izdavanje/lista/po-stranici/20/',
        'https://www.nekretnine.rs/stambeni-objekti/kuce/izdavanje-prodaja/prodaja/lista/po-stranici/20/',
        'https://www.nekretnine.rs/stambeni-objekti/kuce/izdavanje-prodaja/izdavanje/lista/po-stranici/20/'
    ]

    links_visited_counter = 0

    def parse(self, response):
        all_real_estate_links_on_page = response.css('h2.offer-title a::attr(href)')
        
        for real_estate_link_on_page in all_real_estate_links_on_page:
            yield response.follow(real_estate_link_on_page, callback=self.readSingleRealEstate)
        #return ###.

        pagination_link = response.css('a.next-article-button::attr(href)').get()

        #self.redni_broj_stranice += 1       # while testing page data rendering
        #if (self.redni_broj_stranice == 4): # while testing page data rendering
         #   return                          # while testing page data rendering


        if pagination_link is not None:
            yield response.follow(pagination_link, callback=self.parse)
        
        # for i in range(0, 100):
        #     print("ASDASDASD!!!")



    def readSingleRealEstate(self, response):

        item_details_names = response.css('div.property__amenities li::text').extract()
        item_details_values = response.css('div.property__amenities strong::text').extract()
        location_details = response.css('h3.stickyBox__Location::text').extract()
        price = response.css('h4.stickyBox__price::text').extract()

        # self.links_visited_counter += 1
        # if (self.links_visited_counter % 100 == 0):
        #     print(self.links_visited_counter)

        # remove \n and \t characters from strings
        for i in range(0, len(item_details_names)):
            item_details_names[i] = item_details_names[i].replace("\n", "").replace("\t", "").replace(" ","")

        for i in range(0, len(item_details_values)):
            item_details_values[i] = item_details_values[i].replace("\n", "").replace("\t", "").replace(" ","")

        for i in range(0, len(location_details)):
            location_details[i] = location_details[i].replace("\n", "").replace("\t", "").replace(" ","")

        for i in range(0, len(price)):
            price[i] = price[i].replace("\n", "").replace("\t", "").replace(" ","")

        # remove element properties that are just empty strings
        while("" in item_details_names):
            item_details_names.remove("")

        while("" in item_details_values):
            item_details_values.remove("")

        while("" in location_details):
            location_details.remove("")

        while("" in price):
            price.remove("")

        # combine properties names and values where possible
        # if not possible, make properties array with no values
        propertiesWithValues = []
        propertiesWithoutValues = []
        for i in range(0, len(item_details_names)):
            if (i < len(item_details_values)):
                propertiesWithValues.append(item_details_names[i] + item_details_values[i])
            else:
                propertiesWithoutValues.append(item_details_names[i])

        # put data into object items
        realEstateItem = RealEstateItem()
        
        realEstateItem = self.initializeAttributes(realEstateItem)

         # set price details
        if price is not None and len(price) >= 1 and price[0].find('EUR') != -1:
            realEstateItem['cenaNekretnine'] = price[0].split('E')[0]

        realEstateItem = self.addAttributesWithValues(realEstateItem, propertiesWithValues)
        realEstateItem = self.addAttributesWithoutValues(realEstateItem, propertiesWithoutValues)

        # set info about city and city part of real estate
        #print(location_details)
        if location_details is not None and len(location_details) > 0 and location_details[0] is not None and location_details[0].find(',') != -1 and len(location_details[0].split(',')) >= 1:
            realEstateItem['lokacijaGrad'] = location_details[0].split(',')[0]
            
        if location_details is not None and len(location_details) > 0 and location_details[0] is not None and location_details[0].find(',') != -1 and len(location_details[0].split(',')) == 2:
            realEstateItem['lokacijaDeoGrada'] = location_details[0].split(',')[1]
       
        if (realEstateItem['cenaNekretnine'] is not None and realEstateItem['cenaNekretnine'] != 'Cenanaupit'):
            yield realEstateItem
            #print(realEstateItem)
        

        
    # pomocne funkcije

    def initializeAttributes(self, realEstateItem):
        realEstateItem['cenaNekretnine'] = None
        realEstateItem['kvadraturaNekretnine'] = None
        realEstateItem['brojSoba'] = None
        realEstateItem['tipGrejanja'] = None
        realEstateItem['imaParking'] = False
        realEstateItem['ukupnoSpratova'] = None
        realEstateItem['spratnost'] = None
        realEstateItem['uknjizeno'] = False
        realEstateItem['tipNekretnine'] = None
        realEstateItem['tipPonude'] = None
        realEstateItem['godinaIzgradnje'] = None
        realEstateItem['brojKupatila'] = None
        realEstateItem['imaTerasu'] = False
        realEstateItem['imaLadju'] = False
        realEstateItem['imaBalkon'] = False
        realEstateItem['imaPodrum'] = False
        realEstateItem['imaLift'] = False
        realEstateItem['imaKamera'] = False
        realEstateItem['imaAlarm'] = False
        realEstateItem['imaVideoNadzorInterfon'] = False
        realEstateItem['imaInternet'] = False
        realEstateItem['imaTelefon'] = False
        realEstateItem['lokacijaGrad'] = None
        realEstateItem['lokacijaDeoGrada'] = None
        realEstateItem['povrsinaZemljista'] = None

        return realEstateItem


    def addAttributesWithValues(self, realEstateItem, propertiesWithValues):
        for propertyWithValue in propertiesWithValues:
            #print("HEY " + propertyWithValue)
            key = propertyWithValue.split(':')[0]
            value = propertyWithValue.split(':')[1]

            # main details
            if (key == "Kvadratura"): # value = xm2
                realEstateItem['kvadraturaNekretnine'] = value.split('m')[0]
            if (key == "Ukupanbrojsoba"):
                realEstateItem['brojSoba'] = value
            if (key == "Uknjiženo"):
                if (value == "Da"):
                    realEstateItem['uknjizeno'] = True
                else:
                    realEstateItem['uknjizeno'] = False
            if (key == "Ukupanbrojspratova"):
                realEstateItem['ukupnoSpratova'] = value
            if (key == "Spratnost"):
                if (value == "Prizemlje"):
                    realEstateItem['spratnost'] = 0
                elif (value == "Suteren"):
                    realEstateItem['spratnost'] = -1
                elif (value == "Visokoprizemlje"):
                    realEstateItem['spratnost'] = 1
                else:
                    realEstateItem['spratnost'] = value
            if (key == "Površinazemljišta" and value.find('ar') != -1):
                realEstateItem['povrsinaZemljista'] = value.split('a')[0]
            
            # podaci o nekretnini
            if (key == "Kategorija"):
                if ('kuca' in value or 'kuća' in value or 'kuce' in value or 'kuće' in value or
                    'Kuca' in value or 'Kuća' in value or 'Kuce' in value or 'Kuće' in value):
                    realEstateItem['tipNekretnine'] = 'kuca'
                else:
                    if ("stan" in value or "Stan" in value):
                        realEstateItem['tipNekretnine'] = 'stan'

            if (key == "Transakcija"):
                realEstateItem['tipPonude'] = value
            if (key == "Godinaizgradnje"):
                realEstateItem['godinaIzgradnje'] = value
            if (key == "Brojkupatila"):
                realEstateItem['brojKupatila'] = value

        
        return realEstateItem

    
    def addAttributesWithoutValues(self, realEstateItem, propertiesWithoutValues):
        for propertyWithoutValue in propertiesWithoutValues:
            # print("HEY " + propertyWithoutValue)

            key = ""
            value = ""
            #print(propertyWithoutValue)
            if ":" in propertyWithoutValue:
                key = propertyWithoutValue.split(':')[0]
                value = propertyWithoutValue.split(':')[1]
            else:
                key = value = propertyWithoutValue # change later

            # main details
            if ("garaža" in key or "Garaža" in key or "parking" in key or "Parking" in key):
                realEstateItem['imaParking'] = True
            if (key == "Grejanje"):
                realEstateItem['tipGrejanja'] = value
            

            # dodatna opremljenost
            if (key == "Lift"):
                realEstateItem['imaLift'] = True
            if (key == "Terasa"):
                realEstateItem['imaTerasu'] = True
            if (key == "Lađa"):
                realEstateItem['imaLadju'] = True
            if (key == "Balkon"):
                realEstateItem['imaBalkon'] = True
            if (key == "Podrum"):
                realEstateItem['imaPodrum'] = True

            # tehnicka opremljenost
            if (key == "Internet"):
                realEstateItem['imaInternet'] = True
            if (key == "Telefon"):
                realEstateItem['imaTelefon'] = True

            # sigurnosna oprema
            if (key == "Alarm"):
                realEstateItem['imaAlarm'] = True
            if (key == "Kamera"):
                realEstateItem['imaKamera'] = True
            if (key == "Videonadzor/Interfon"):
                realEstateItem['imaVideoNadzorInterfon'] = True


        return realEstateItem