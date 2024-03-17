import mysql.connector
from datetime import datetime
import sys

class DatabaseFilter:

    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host = '127.0.0.1',
            port = '3306',
            user = 'root',
            passwd = '12345678',
            database = 'nekretnine',
            ssl_disabled =  True
        )
        self.curr = self.conn.cursor()


    def filter_db(self):
        self.filter_real_estate_types()
        self.filter_houses()
        self.filter_flats()
        self.curr.close()
        self.conn.close()


    def filter_real_estate_types(self): # delete types that are neither 'kuca' nor 'stan'
        self.curr.execute("""delete from nekretnine_db_zad2
            where tipNekretnine is null or (tipNekretnine != 'kuca' and tipNekretnine != 'stan')
                    or kvadraturaNekretnine is null or kvadraturaNekretnine > 10000
        """)
        self.conn.commit()

    def filter_houses(self):
        self.curr.execute("""delete from nekretnine_db_zad2
            where tipNekretnine = 'kuca' and (brojSoba is null or brojKupatila is null
                or (lokacijaGrad is null and lokacijaDeoGrada is null) or tipPonude is null)
        """)
        self.conn.commit()

    def filter_flats(self):
        self.curr.execute("""delete from nekretnine_db_zad2
            where tipNekretnine = 'stan' and (brojSoba is null or brojKupatila is null
                or (lokacijaGrad is null and lokacijaDeoGrada is null)  or tipPonude is null)
        """)
        self.conn.commit()



class DataAnalizer:

    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host = '127.0.0.1',
            port = '3306',
            user = 'root',
            passwd = '12345678',
            database = 'nekretnine',
            ssl_disabled =  True
        )
        self.curr = self.conn.cursor()

    def get_number_of_selling_and_renting(self): # stavka a)

        print("STAVKA A: Izlistati koliki je broj nekretnina za prodaju, a koliki je broj koji se iznajmljuju")
        # number of selling
        self.curr.execute("""select count(*) from nekretnine_db_zad2 where tipPonude = 'Prodaja' """)
        data = self.curr.fetchall()
        print("Broj nekretnina koje se prodaju: " + str(data[0][0]))

        # number of renting
        self.curr.execute("""select count(*) from nekretnine_db_zad2 where tipPonude = 'Izdavanje' """)
        data = self.curr.fetchall()
        print("Broj nekretnina koje se iznajmljuju: " + str(data[0][0]))
        print("\n")


    def count_real_estates_for_sale_per_city(self): # stavka b)

        self.curr.execute("""select lokacijaGrad, count(*) as 'Broj nekretnina za prodaju'
                from nekretnine_db_zad2
                where tipPonude = "Prodaja"
                group by (lokacijaGrad)
                order by count(*) desc""")
        data = self.curr.fetchall()
        print("STAVKA B: izlistati koliko nekretnina se prodaje u svakom od gradova")
        for row in data:
            print(str(row[0]) + " -> " + str(row[1]))

        print("\n")

    
    def count_registered_unregistered_houses_flats(self): # stavka c)

        self.curr.execute("""select 
            (select count(*) from nekretnine_db_zad2 where tipNekretnine = 'kuca' and uknjizeno = True) as 'Broj uknjizenih kuca',
            (select count(*) from nekretnine_db_zad2 where tipNekretnine = 'kuca' and uknjizeno = False) as 'Broj neuknjizenih kuca',
            (select count(*) from nekretnine_db_zad2 where tipNekretnine = 'stan' and uknjizeno = True) as 'Broj uknjizenih stanova',
            (select count(*) from nekretnine_db_zad2 where tipNekretnine = 'stan' and uknjizeno = False) as 'Broj neuknjizenih stanova'""")

        data = self.curr.fetchall()
        print("STAVKA C: izlistati koliko je uknjiženih, a koliko neuknjiženih kuća, a koliko stanova")
        print("Broj uknjizenih kuca: " + str(data[0][0]))
        print("Broj neuknjizenih kuca: " + str(data[0][1]))
        print("Broj uknjizenih stanova: " + str(data[0][2]))
        print("Broj neuknjizenih stanova: " + str(data[0][3]))
        print('\n')


    def get_30_most_expensive_real_estates_by_type(self, real_estate_type): # pomocna funkcija za stavku d)
        self.curr.execute("""select cenaNekretnine
            from nekretnine_db_zad2
            where tipNekretnine = %s
            order by cenaNekretnine desc
            limit 30""", (str(real_estate_type), ))
        data = self.curr.fetchall()
        
        if (str(real_estate_type) == 'kuca'):
            print("Lista 30 najskupljih kuća: ")
        if (str(real_estate_type) == 'stan'):
            print("Lista 30 najskupljih stanova: ")
        for row in data:
            print(row[0])


    def get_30_most_expensive_houses_flats(self): # stavka d)
        print("STAVKA D: prikazati rang listu prvih 30 najskupljih kuća koje se prodaju, i 30 najskupljih stanova koji se prodaju u Srbiji")
        self.get_30_most_expensive_real_estates_by_type('kuca')
        print('\n')
        self.get_30_most_expensive_real_estates_by_type('stan')
        print('\n')

    
    def get_100_biggest_real_estates_by_type(self, real_estate_type): # pomocna funkcija za stavku e)
        self.curr.execute("""select kvadraturaNekretnine
            from nekretnine_db_zad2
            where tipNekretnine = %s
            order by kvadraturaNekretnine desc
            limit 100""", (real_estate_type, ))
        data = self.curr.fetchall()
        
        if (str(real_estate_type) == 'kuca'):
            print("Lista 100 najvećih kuća: ")
        if (str(real_estate_type) == 'stan'):
            print("Lista 100 najvećih stanova: ")
        for row in data:
            print(row[0])


    def get_100_biggest_houses_flats(self): # stavka e)
        print("STAVKA E: prikazati rang listu prvih 100 najvećih kuća i 100 najvećih stanova po kvadraturi")
        self.get_100_biggest_real_estates_by_type('kuca')
        print('\n')
        self.get_100_biggest_real_estates_by_type('stan')
        print('\n')


    def get_2022_2023_real_estates_data_parsing(self): # pomocna funkcija za stavku f)
        self.curr.execute("""select tipNekretnine, godinaIzgradnje, tipPonude, cenaNekretnine
            from nekretnine_db_zad2
            where (godinaIzgradnje = 2022 or godinaIzgradnje = 2023)
            order by cenaNekretnine desc""")
        data = self.curr.fetchall()

        for row in data:
            print(str(row[0]) + " - " + str(row[1]) + " - " + str(row[2]) + " - " + str(row[3]))


    def get_2022_2023_real_estates(self): # stavka f)
        print("STAVKA F: prikazati rang listu svih nekretnina izgrađenih u 2022. ili 2023. godini, i izlistati ih opadajuće prema ceni prodaje, odnosno ceni iznajmljivanja")
        self.get_2022_2023_real_estates_data_parsing()
        print('\n')


    def get_top_30_by_number_of_rooms(self): # pomocna funkcija za stavku g)
        self.curr.execute("""select tipNekretnine, brojSoba
            from nekretnine_db_zad2
            order by brojSoba desc
            limit 30""")
        data = self.curr.fetchall()

        print("▪ najveći broj soba unutar nekretnine")
        for row in data:
            print(str(row[0]) + " - " + str(row[1]) + " soba")


    def get_top_30_flats_by_square_meters(self): # pomocna funkcija za stavku g)
        self.curr.execute("""select kvadraturaNekretnine
            from nekretnine_db_zad2
            where tipNekretnine = 'stan'
            order by kvadraturaNekretnine desc
            limit 30""")
        data = self.curr.fetchall()

        print("▪ najveću kvadraturu (samo za stanove)")
        for row in data:
            print(str(row[0]) + " m^2")
    

    def get_top_30_houses_by_acres(self): # pomocna funkcija za stavku g)
        self.curr.execute("""select povrsinaZemljista
            from nekretnine_db_zad2
            where tipNekretnine = 'kuca'
            order by povrsinaZemljista desc
            limit 30""")
        data = self.curr.fetchall()

        print("▪ najveću površinu zemljišta (samo za kuće)")
        for row in data:
            print(str(row[0]) + " ari")


    def get_top_30_by_categories(self): # stavka g)
        print("STAVKA G: prikazati nekretnine (Top30) koje imaju:")
        self.get_top_30_by_number_of_rooms()
        print('\n')
        self.get_top_30_flats_by_square_meters()
        print('\n')
        self.get_top_30_houses_by_acres()
        print('\n')


if __name__ == "__main__":
    with open('zadatak2log.txt', 'w', encoding='utf-8') as file:
        # Redirect the standard output (stdout) to the file
        sys.stdout = file
        # part for filtering database after scraping data
        print("Begin filtering database...   [timestamp:  " + str(datetime.now()) + " ]")
        databaseFilter = DatabaseFilter()
        databaseFilter.filter_db()
        print("Database filtering complete!   [timestamp:  " + str(datetime.now()) + " ]")

        # part for analizing data, according to requirements by task 2
        databaseAnalizing = DataAnalizer()
        print("\n")
        databaseAnalizing.get_number_of_selling_and_renting()
        databaseAnalizing.count_real_estates_for_sale_per_city()
        databaseAnalizing.count_registered_unregistered_houses_flats()
        databaseAnalizing.get_30_most_expensive_houses_flats()
        databaseAnalizing.get_100_biggest_houses_flats()
        databaseAnalizing.get_2022_2023_real_estates()
        databaseAnalizing.get_top_30_by_categories()

