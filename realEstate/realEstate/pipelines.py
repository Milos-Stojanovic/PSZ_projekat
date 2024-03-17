# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# Scraped data -> Item Containers -> Pipelines -> SQL/Mongo database

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector

class RealEstatePipeline:

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = None
        self.curr = None
        try:
            self.conn = mysql.connector.connect(
                host = '127.0.0.1',
                port = '3306',
                user = 'root',
                passwd = '12345678',
                database = 'nekretnine',
                ssl_disabled =  True
            )
            print("Connected to the database!")
            self.curr = self.conn.cursor()
        except Exception :
            print("Error while connecting to MySQL", Exception)


    def create_table(self):
        self.curr.execute("""drop table if exists nekretnine_db""")
        self.curr.execute("""create table nekretnine_db(
                cenaNekretnine double,
                kvadraturaNekretnine double,
                brojSoba int,
                tipGrejanja text,
                imaParking boolean,
                ukupnoSpratova int,
                spratnost int,
                uknjizeno boolean,
                tipNekretnine text,
                tipPonude text,
                godinaIzgradnje int,
                brojKupatila int,
                imaTerasu boolean,
                imaLadju boolean,
                imaBalkon boolean,
                imaPodrum boolean,
                imaLift boolean,
                imaKamera boolean,
                imaAlarm boolean,
                imaVideoNadzorInterfon boolean,
                imaInternet boolean,
                imaTelefon boolean,
                lokacijaGrad text,
                lokacijaDeoGrada text,
                povrsinaZemljista double
            )""")
    
    def process_item(self, item, spider):
        self.store_db(item)
        #print("Pipeline: " + item['cenaNekretnine'])
        return item

    def store_db(self, item):
        self.curr.execute("""insert into nekretnine_db values (%s, %s, %s, %s,
                                %s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,
                                %s, %s, %s, %s,%s, %s, %s, %s, %s)""",(
            item['cenaNekretnine'],
            item['kvadraturaNekretnine'],
            item['brojSoba'],
            item['tipGrejanja'],
            item['imaParking'],
            item['ukupnoSpratova'],
            item['spratnost'],
            item['uknjizeno'],
            item['tipNekretnine'],
            item['tipPonude'],
            item['godinaIzgradnje'],
            item['brojKupatila'],
            item['imaTerasu'],
            item['imaLadju'],
            item['imaBalkon'],
            item['imaPodrum'],
            item['imaLift'],
            item['imaKamera'],
            item['imaAlarm'],
            item['imaVideoNadzorInterfon'],
            item['imaInternet'],
            item['imaTelefon'],
            item['lokacijaGrad'],
            item['lokacijaDeoGrada'],
            item['povrsinaZemljista']
        ))
        self.conn.commit()