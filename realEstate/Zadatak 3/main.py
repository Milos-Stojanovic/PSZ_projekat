import mysql.connector
from datetime import datetime
import sys
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html

class DataCollector:

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

    def get_10_most_common_Belgrade_areas(self): # stavka a)
        self.curr.execute("""select lokacijaDeoGrada, count(*)
                from nekretnine_db_zad2
                where lokacijaGrad = 'Beograd'
                group by lokacijaDeoGrada
                order by count(*) desc
                limit 10""")

        data = self.curr.fetchall()
        cities = ['a'] * 10
        number_of_real_estates = [0] * 10
        for i in range(0, 10):
            cities[i] = data[i][0]
            number_of_real_estates[i] = data[i][1]

        return cities, number_of_real_estates


    def get_flats_for_sale_by_meters_squared(self): # stavka b)
        self.curr.execute("""select 
                (select count(*) from nekretnine_db_zad2 where tipNekretnine = 'stan' and tipPonude = 'Prodaja' and kvadraturaNekretnine <= 35) as '<=35m^2'
                ,(select count(*) from nekretnine_db_zad2 where tipNekretnine = 'stan' and tipPonude = 'Prodaja' and kvadraturaNekretnine >= 35 and kvadraturaNekretnine <= 50) as '36-50m^2'
                ,(select count(*) from nekretnine_db_zad2 where tipNekretnine = 'stan' and tipPonude = 'Prodaja' and kvadraturaNekretnine >= 51 and kvadraturaNekretnine <= 65) as '51-65m^2'
                ,(select count(*) from nekretnine_db_zad2 where tipNekretnine = 'stan' and tipPonude = 'Prodaja' and kvadraturaNekretnine >= 66 and kvadraturaNekretnine <= 80) as '66-80m^2'
                ,(select count(*) from nekretnine_db_zad2 where tipNekretnine = 'stan' and tipPonude = 'Prodaja' and kvadraturaNekretnine >= 81 and kvadraturaNekretnine <= 95) as '81-95m^2'
                ,(select count(*) from nekretnine_db_zad2 where tipNekretnine = 'stan' and tipPonude = 'Prodaja' and kvadraturaNekretnine >= 96 and kvadraturaNekretnine <= 110) as '96-110m^2'
                ,(select count(*) from nekretnine_db_zad2 where tipNekretnine = 'stan' and tipPonude = 'Prodaja' and kvadraturaNekretnine >= 111) as '>=111m^2'
            """)

        data = self.curr.fetchall()

        column_names = [column[0] for column in self.curr.description]
        number_of_flats = [0] * 7
        for i in range(0, 7):
            number_of_flats[i] = data[0][i]

        return column_names, number_of_flats


    def get_real_estates_by_decades(self): # stavka c)
        self.curr.execute("""select 
                    (select count(*) from nekretnine_db_zad2 where  godinaIzgradnje >= 1951 and godinaIzgradnje <= 1960) as '1951-1960'
                    ,(select count(*) from nekretnine_db_zad2 where godinaIzgradnje >= 1961 and godinaIzgradnje <= 1970) as '1961-1970'
                    ,(select count(*) from nekretnine_db_zad2 where godinaIzgradnje >= 1971 and godinaIzgradnje <= 1980) as '1971-1980'
                    ,(select count(*) from nekretnine_db_zad2 where godinaIzgradnje >= 1981 and godinaIzgradnje <= 1990) as '1981-1990'
                    ,(select count(*) from nekretnine_db_zad2 where godinaIzgradnje >= 1991 and godinaIzgradnje <= 2000) as '1991-2000'
                    ,(select count(*) from nekretnine_db_zad2 where godinaIzgradnje >= 2001 and godinaIzgradnje <= 2010) as '2001-2010'
                    ,(select count(*) from nekretnine_db_zad2 where godinaIzgradnje >= 2011 and godinaIzgradnje <= 2020) as '2011-2020'
                """)

        data = self.curr.fetchall()

        column_names = [column[0] for column in self.curr.description]
        number_of_real_estates_by_decade = [0] * 7
        for i in range(0, 7):
            number_of_real_estates_by_decade[i] = data[0][i]

        return column_names, number_of_real_estates_by_decade


    def get_top_5_cities_by_real_estate_number(self): # stavka d)
        self.curr.execute("""select ndbz2.lokacijaGrad
                from nekretnine_db_zad2 ndbz2
                group by ndbz2.lokacijaGrad
                order by count(*) desc
                limit 5
            """)

        data = self.curr.fetchall()

        cities = ['a'] * 5
        for i in range(0, 5):
            cities[i] = data[i][0]

        return cities

    
    def get_real_estate_number_and_percentage__for_city(self, city): # stavka d)
        self.curr.execute("""select
                (select count(*) from nekretnine_db_zad2 where lokacijaGrad = %s and tipPonude='Prodaja') as 'Broj za prodaju'
                ,(select count(*) from nekretnine_db_zad2 where lokacijaGrad = %s and tipPonude='Izdavanje') as 'Broj za iznajmljivanje'
                ,(select count(*) from nekretnine_db_zad2 where lokacijaGrad = %s and tipPonude='Prodaja') / (select count(*) from nekretnine_db_zad2 where lokacijaGrad = %s)*100 as 'Procenat za prodaju'
                ,(select count(*) from nekretnine_db_zad2 where lokacijaGrad = %s and tipPonude='Izdavanje') / (select count(*) from nekretnine_db_zad2 where lokacijaGrad = %s)*100 as 'Procenat za iznajmljivanje'
            """, (city, city, city, city, city, city))

        data = self.curr.fetchall()

        information = [0] * 4
        for i in range(0, 4):
            information[i] = data[0][i]

        return information


    def get_total_number_and_perc_sold_based_on_value(self): # stavka e)
        self.curr.execute("""select 
                (select count(*) from nekretnine_db_zad2 where tipPonude = 'Prodaja' and cenaNekretnine < 50000) as 'Broj <50000'
                ,(select count(*) from nekretnine_db_zad2 where tipPonude = 'Prodaja' and cenaNekretnine < 50000)/(select count(*) from nekretnine_db_zad2 where tipPonude = 'Prodaja')*100 as 'Procenat <50000'
                ,(select count(*) from nekretnine_db_zad2 where tipPonude = 'Prodaja' and cenaNekretnine >= 50000 and cenaNekretnine < 100000) as 'Broj [50000,100000)'
                ,(select count(*) from nekretnine_db_zad2 where tipPonude = 'Prodaja' and cenaNekretnine >= 50000 and cenaNekretnine < 100000)/(select count(*) from nekretnine_db_zad2 where tipPonude = 'Prodaja')*100 as 'Procenat [50000,100000)'
                ,(select count(*) from nekretnine_db_zad2 where tipPonude = 'Prodaja' and cenaNekretnine >= 100000 and cenaNekretnine < 150000) as 'Broj [100000,150000)'
                ,(select count(*) from nekretnine_db_zad2 where tipPonude = 'Prodaja' and cenaNekretnine >= 100000 and cenaNekretnine < 150000)/(select count(*) from nekretnine_db_zad2 where tipPonude = 'Prodaja')*100 as 'Procenat [100000,150000)'
                ,(select count(*) from nekretnine_db_zad2 where tipPonude = 'Prodaja' and cenaNekretnine >= 150000 and cenaNekretnine < 200000) as 'Broj [150000,200000)'
                ,(select count(*) from nekretnine_db_zad2 where tipPonude = 'Prodaja' and cenaNekretnine >= 150000 and cenaNekretnine < 200000)/(select count(*) from nekretnine_db_zad2 where tipPonude = 'Prodaja')*100 as 'Procenat [150000,200000)'
                ,(select count(*) from nekretnine_db_zad2 where tipPonude = 'Prodaja' and cenaNekretnine >= 200000 and cenaNekretnine < 500000) as 'Broj [200000,500000)'
                ,(select count(*) from nekretnine_db_zad2 where tipPonude = 'Prodaja' and cenaNekretnine >= 200000 and cenaNekretnine < 500000)/(select count(*) from nekretnine_db_zad2 where tipPonude = 'Prodaja')*100 as 'Procenat [200000,500000)'
                ,(select count(*) from nekretnine_db_zad2 where tipPonude = 'Prodaja' and cenaNekretnine >= 500000) as 'Broj >500000'
                ,(select count(*) from nekretnine_db_zad2 where tipPonude = 'Prodaja' and cenaNekretnine >= 500000)/(select count(*) from nekretnine_db_zad2 where tipPonude = 'Prodaja')*100 as 'Procenat <50000'
             """)

        data = self.curr.fetchall()

        information = [0] * 12
        for i in range(0, 12):
            information[i] = data[0][i]

        return information


    def get_Belgrade_number_with_without_parking(self): # stavka f)
        self.curr.execute("""select
            (select count(*) from nekretnine_db_zad2 where lokacijaGrad = 'Beograd' and imaParking = True) as 'Nekretnine sa parkingom u Beogradu'
            ,(select count(*) from nekretnine_db_zad2 where lokacijaGrad = 'Beograd') as 'Ukupno nekretnina u Beogradu'
        """)

        data = self.curr.fetchall()

        information = [0] * 2
        for i in range(0, 2):
            information[i] = data[0][i]

        return information


data_collector = DataCollector()
app = dash.Dash()


stavka_a_x, stavka_a_y = data_collector.get_10_most_common_Belgrade_areas()
stavka_b_x, stavka_b_y = data_collector.get_flats_for_sale_by_meters_squared()
stavka_c_x, stavka_c_y = data_collector.get_real_estates_by_decades()
# informacije za stavku d
top_5_cities_with_most_real_estates = data_collector.get_top_5_cities_by_real_estate_number()
stavka_d1_y = data_collector.get_real_estate_number_and_percentage__for_city(top_5_cities_with_most_real_estates[0])
stavka_d2_y = data_collector.get_real_estate_number_and_percentage__for_city(top_5_cities_with_most_real_estates[1])
stavka_d3_y = data_collector.get_real_estate_number_and_percentage__for_city(top_5_cities_with_most_real_estates[2])
stavka_d4_y = data_collector.get_real_estate_number_and_percentage__for_city(top_5_cities_with_most_real_estates[3])
stavka_d5_y = data_collector.get_real_estate_number_and_percentage__for_city(top_5_cities_with_most_real_estates[4])
# informacije za stavku e
stavka_e_y = data_collector.get_total_number_and_perc_sold_based_on_value()
# informacije za stavku f
stavka_f_y = data_collector.get_Belgrade_number_with_without_parking()

app.layout = html.Div([
    # grafik za stavku a)
    dcc.Graph(
        id = 'stavka-a',
        figure = {
            'data': [
                {'x' : stavka_a_x, 'y': stavka_a_y, 'type':'bar', 'name':'First chart'}
            ],
            'layout': {
                'title': '10 delova Beograda sa najvise nekretnina u ponudi'
            }
        }
    ),

    # grafik za stavku b)
    dcc.Graph(
        id = 'stavka-b',
        figure = {
            'data': [
                {'x' : stavka_b_x, 'y': stavka_b_y, 'type':'bar', 'name':'Second chart'}
            ],
            'layout': {
                'title': 'Broj stanova za prodaju po kvadraturi'
            }
        }
    ),

    # grafik za stavku c)
    dcc.Graph(
        id = 'stavka-c',
        figure = {
            'data': [
                {'x' : stavka_c_x, 'y': stavka_c_y, 'type':'bar', 'name':'Third chart'}
            ],
            'layout': {
                'title': 'Broj izgradjenih nekretnina po dekadama'
            }
        }
    ),

    html.Br(),
    html.Br(),

    # 1. grafik za stavku d)
     html.Div([
        
        dcc.Graph(
            id = 'stavka-d-1.1',
            figure = {
                'data': [
                    {'x' : ['Broj za prodaju', 'Broj za izdavanje'], 'y': stavka_d1_y[0:2], 'type':'bar', 'name':'Fourth chart'}
                ],
                'layout': {
                    'title': 'Odnos broja nekretnina za prodaju i izdavanje - ' + str(top_5_cities_with_most_real_estates[0])
                }
            }, style={'width': '49%', 'display': 'inline-block'}
        ),

        dcc.Graph(
            id = 'stavka-d-1.2',
            figure = {
                'data': [
                    {'x' : ['Procenat za prodaju', 'Procenat za izdavanje'], 'y': stavka_d1_y[2:4], 'type':'bar', 'name':'Fifth chart'}
                ],
                'layout': {
                    'title': 'Odnos procenta nekretnina za prodaju i izdavanje - ' + str(top_5_cities_with_most_real_estates[0])
                }
            }, style={'width': '49%', 'display': 'inline-block'}
        )

    ]),

    # 2. grafik za stavku d)
     html.Div([
        
        dcc.Graph(
            id = 'stavka-d-2.1',
            figure = {
                'data': [
                    {'x' : ['Broj za prodaju', 'Broj za izdavanje'], 'y': stavka_d2_y[0:2], 'type':'bar', 'name':'Sixth chart'}
                ],
                'layout': {
                    'title': 'Odnos broja nekretnina za prodaju i izdavanje - ' + str(top_5_cities_with_most_real_estates[1])
                }
            }, style={'width': '49%', 'display': 'inline-block'}
        ),

        dcc.Graph(
            id = 'stavka-d-2.2',
            figure = {
                'data': [
                    {'x' : ['Procenat za prodaju', 'Procenat za izdavanje'], 'y': stavka_d2_y[2:4], 'type':'bar', 'name':'Seventh chart'}
                ],
                'layout': {
                    'title': 'Odnos procenta nekretnina za prodaju i izdavanje - ' + str(top_5_cities_with_most_real_estates[1])
                }
            }, style={'width': '49%', 'display': 'inline-block'}
        )

    ]),

    # 3. grafik za stavku d)
     html.Div([
        
        dcc.Graph(
            id = 'stavka-d-3.1',
            figure = {
                'data': [
                    {'x' : ['Broj za prodaju', 'Broj za izdavanje'], 'y': stavka_d3_y[0:2], 'type':'bar', 'name':'Eigth chart'}
                ],
                'layout': {
                    'title': 'Odnos broja nekretnina za prodaju i izdavanje - ' + str(top_5_cities_with_most_real_estates[2])
                }
            }, style={'width': '49%', 'display': 'inline-block'}
        ),

        dcc.Graph(
            id = 'stavka-d-3.2',
            figure = {
                'data': [
                    {'x' : ['Procenat za prodaju', 'Procenat za izdavanje'], 'y': stavka_d3_y[2:4], 'type':'bar', 'name':'Ninth chart'}
                ],
                'layout': {
                    'title': 'Odnos procenta nekretnina za prodaju i izdavanje - ' + str(top_5_cities_with_most_real_estates[2])
                }
            }, style={'width': '49%', 'display': 'inline-block'}
        )

    ]),

    # 4. grafik za stavku d)
     html.Div([
        
        dcc.Graph(
            id = 'stavka-d-4.1',
            figure = {
                'data': [
                    {'x' : ['Broj za prodaju', 'Broj za izdavanje'], 'y': stavka_d4_y[0:2], 'type':'bar', 'name':'Tenth chart'}
                ],
                'layout': {
                    'title': 'Odnos broja nekretnina za prodaju i izdavanje - ' + str(top_5_cities_with_most_real_estates[3])
                }
            }, style={'width': '49%', 'display': 'inline-block'}
        ),

        dcc.Graph(
            id = 'stavka-d-4.2',
            figure = {
                'data': [
                    {'x' : ['Procenat za prodaju', 'Procenat za izdavanje'], 'y': stavka_d4_y[2:4], 'type':'bar', 'name':'Eleventh chart'}
                ],
                'layout': {
                    'title': 'Odnos procenta nekretnina za prodaju i izdavanje - ' + str(top_5_cities_with_most_real_estates[3])
                }
            }, style={'width': '49%', 'display': 'inline-block'}
        )

    ]),

    # 5. grafik za stavku d)
     html.Div([
        
        dcc.Graph(
            id = 'stavka-d-5.1',
            figure = {
                'data': [
                    {'x' : ['Broj za prodaju', 'Broj za izdavanje'], 'y': stavka_d5_y[0:2], 'type':'bar', 'name':'Twelveth chart'}
                ],
                'layout': {
                    'title': 'Odnos broja nekretnina za prodaju i izdavanje - ' + str(top_5_cities_with_most_real_estates[4])
                }
            }, style={'width': '49%', 'display': 'inline-block'}
        ),

        dcc.Graph(
            id = 'stavka-d-5.2',
            figure = {
                'data': [
                    {'x' : ['Procenat za prodaju', 'Procenat za izdavanje'], 'y': stavka_d5_y[2:4], 'type':'bar', 'name':'Thirteenth chart'}
                ],
                'layout': {
                    'title': 'Odnos procenta nekretnina za prodaju i izdavanje - ' + str(top_5_cities_with_most_real_estates[4])
                }
            }, style={'width': '49%', 'display': 'inline-block'}
        )

    ]),

    html.Br(),
    html.Br(),

    # 1. grafik za stavku e)
     html.Div([
        
        dcc.Graph(
            id = 'stavka-e-1.1',
            figure = {
                'data': [
                    {'x' : ['<50000', 
                    '50000-100000', 
                    '100000-150000', 
                    '150000-200000', 
                    '200000-500000', 
                    '>500000'], 'y': [
                        stavka_e_y[0],
                        stavka_e_y[2],
                        stavka_e_y[4],
                        stavka_e_y[6],
                        stavka_e_y[8],
                        stavka_e_y[10],
                        ], 'type':'bar', 'name':'Fourth chart'}
                ],
                'layout': {
                    'title': 'Odnos broja svih nekretnina za prodaju u zavisnosti od cene'
                }
            }, style={'width': '49%', 'display': 'inline-block'}
        ),

        dcc.Graph(
            id = 'stavka-e',
            figure = {
                'data': [
                    {'x' : ['<50000', 
                    '50000-100000', 
                    '100000-150000', 
                    '150000-200000', 
                    '200000-500000', 
                    '>500000'], 'y': [
                        stavka_e_y[1],
                        stavka_e_y[3],
                        stavka_e_y[5],
                        stavka_e_y[7],
                        stavka_e_y[9],
                        stavka_e_y[11],
                    ], 'type':'bar', 'name':'Fifth chart'}
                ],
                'layout': {
                    'title': 'Odnos procenta nekretnina za prodaju u zavisnosti od cene'
                }
            }, style={'width': '49%', 'display': 'inline-block'}
        )

    ]),

    # grafik za stavku f)
    dcc.Graph(
        id = 'stavka-f',
        figure = {
            'data': [
                {'x' : ['Broj nekretnina sa parkingom', 'Ukupan broj nekretnina'], 'y': stavka_f_y, 'type':'bar', 'name':'Second chart'}
            ],
            'layout': {
                'title': 'Broj nekretnina za prodaju koje imaju parking, u odnosu na ukupan broj nekretnina za prodaju (samo za Beograd)'
            }
        }
    ),

])

if __name__ == "__main__":
    # with open('zadatak3log.txt', 'w', encoding='utf-8') as file:
    #     # Redirect the standard output (stdout) to the file
    #     sys.stdout = file
    #     # part for filtering database after scraping data
    #     print("Begin filtering database...   [timestamp:  " + str(datetime.now()) + " ]")
    #     databaseFilter = DatabaseFilter()
    #     databaseFilter.filter_db()
    #     print("Database filtering complete!   [timestamp:  " + str(datetime.now()) + " ]")

    #     # part for analizing data, according to requirements by task 2
    #     databaseAnalizing = DataAnalizer()
    #     print("\n")
    #     databaseAnalizing.get_number_of_selling_and_renting()
    #     databaseAnalizing.count_real_estates_for_sale_per_city()
    #     databaseAnalizing.count_registered_unregistered_houses_flats()
    #     databaseAnalizing.get_30_most_expensive_houses_flats()
    #     databaseAnalizing.get_100_biggest_houses_flats()
    #     databaseAnalizing.get_2022_2023_real_estates()
    #     databaseAnalizing.get_top_30_by_categories()
    app.run_server(port=4050)

