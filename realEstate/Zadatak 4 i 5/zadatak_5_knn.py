import mysql.connector
import math
import random
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import geocoder
import re
import csv
import pandas as pd
import numpy as np
import bisect

class KNN_Model():

    def __init__(self):

        self.euclidean_distances = []
        self.manhattan_distances = []
        self.k = 0
        self.counter = 0

        self.initialize_all_features()
        self.get_data_from_database(False)
        self.calculate_k()
        #print(self.k)


    def get_data_from_database(self, yes):
        if yes:
            self.create_connection()
            self.get_all_needed_data_from_database()
        else:
            self.load_data_from_file();

    def load_data_from_file(self):
        df = pd.read_csv('data.csv')
        df = df[['distance', 'size', 'num_of_rooms', 'floor', 'price']].astype(float)
        df.columns = range(df.shape[1])

        data = df.to_dict(orient='list')

        self.X = dict(list(data.items())[:-1])
        self.Y = data[len(self.X)]
        self.Y = [self.classify(y) for y in self.Y]
        print(self.Y)

        self.n_features = len(self.X)
        self.m_samples = len(self.X[0])

    def initialize_all_features(self):
        self.Y = []
        self.udaljenostOdCentra = []
        self.kvadraturaNekretnine = []
        self.brojSoba = []
        self.spratnost = []

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

    def get_location_coordinates(self, location_name):
        location = geocoder.osm(location_name)
        if location.ok:
            return location.latlng
        else:
            self.unsuccessfulLocationCalculations.append(location_name)
            return None

    def calculate_distance(self, city_center_coordinates, location_coordinates):
        return geodesic(city_center_coordinates, location_coordinates).meters

    def calculateDistance(self, lokacija):
        city_center_name = "Belgrade, Serbia"
        city_center_coordinates = self.get_location_coordinates(city_center_name)
        #print(self.split_on_uppercase(lokacija))
        other_location_name = self.split_on_uppercase(lokacija)
        other_location_coordinates = self.get_location_coordinates(other_location_name)

        distance = None;

        if city_center_coordinates and other_location_coordinates:
            distance = self.calculate_distance(city_center_coordinates, other_location_coordinates)

        self.counter += 1
        if self.counter % 10 == 0:
            print(self.counter)

        return distance

    def split_on_uppercase(self, input_string):
    # Use regular expression to find positions where an uppercase character appears
        
        if "NoviBeograd" in input_string or "Novibeograd" in input_string or "novibeograd" in input_string or "noviBeograd" in input_string:
            # Remove substrings encapsulated within parentheses
            input_string = re.sub(r'\([^)]*\)', '', input_string)

        # Check if the input string contains "Savskivenac"
        if "Savskivenac" in input_string:
            # Replace "Savskivenac" with "Savski venac"
            input_string = input_string.replace("Savskivenac", "Savski venac")

        matches = re.finditer('[A-Z]+|\d+', input_string)

        # Create a list of slices to split the string at uppercase characters
        indices = [match.start() for match in matches]
        substrings = [input_string[i:j] for i, j in zip([0] + indices, indices + [None])]

        # Concatenate the substrings with spaces between them
        result = ' '.join(substrings)

        return result

    def get_all_needed_data_from_database(self):
        with open("data.csv", mode="w", newline='') as file:

            # Create a CSV writer object
            csv_writer = csv.writer(file)

            csv_writer.writerow(["distance","size","num_of_rooms","floor","price"])

            self.curr.execute("""
                select cenaNekretnine, kvadraturaNekretnine, tipNekretnine, brojSoba, brojKupatila, 
                    uknjizeno, imaParking, imaLift, imaTerasu, imaBalkon, imaKamera,
                    imaAlarm, imaVideoNadzorInterfon, imaInternet, imaTelefon, spratnost, lokacijaDeoGrada
                from nekretnine_db_zad2
                where tipPonude = 'Prodaja'
                and (lokacijaDeoGrada like '%Zvezdara%'
                    or lokacijaDeoGrada like '%Bulevarkr.aleksandra%'
                    or lokacijaDeoGrada like '%Cvetkova%'
                    or lokacijaDeoGrada like '%Đeram%'
                    or lokacijaDeoGrada like '%Vukovspomenik%'
                    or lokacijaDeoGrada like '%Lion%'
                or lokacijaDeoGrada like '%Vračar%'
                    or lokacijaDeoGrada like '%Crvenikrst%'
                    or lokacijaDeoGrada like '%Slavija%'
                    or lokacijaDeoGrada like '%Čubura%'	
                    or lokacijaDeoGrada like '%Južnibulevar%'	
                or lokacijaDeoGrada like '%Starigrad%'
                    or lokacijaDeoGrada like '%Dorćol%'
                    or lokacijaDeoGrada like '%Skadarlija%'
                or lokacijaDeoGrada like '%Savskivenac%'
                    or lokacijaDeoGrada like '%Beogradnavodi%'
                    or lokacijaDeoGrada like '%Senjak%'
                    or lokacijaDeoGrada like '%Zelenivenac%'
                or lokacijaDeoGrada like '%Novibeograd%'
                    or lokacijaDeoGrada like '%Ledine%'
                or lokacijaDeoGrada like 'Kalenićpijaca')
                    and brojSoba > 0 and spratnost is not null
            """)

            data = self.curr.fetchall()
            for row in data:
                distance = self.calculateDistance(row[16])
                if distance != None and distance < 1000000:
                    self.Y.append(round(row[0]))
                    self.kvadraturaNekretnine.append(round(row[1]))
                    self.brojSoba.append(row[3])
                    self.spratnost.append(row[15])
                    self.udaljenostOdCentra.append(round(distance))
                
            
        
            # Write each sublist as a row in the CSV file
            csv_writer.writerows(list(zip(
                self.udaljenostOdCentra,
                self.kvadraturaNekretnine,
                self.brojSoba,
                self.spratnost,
                self.Y
            )))
        
        # Combine features into one list
        self.X = list(zip(
            self.kvadraturaNekretnine,
            self.brojSoba,
            self.spratnost,
            self.udaljenostOdCentra
        ))

        self.Y = [self.classify(y) for y in self.Y]
 
    def classify(self, y):
        # class 1   <= 49 999 
        # class 2   50 000 - 99 999 
        # class 3   100 000 - 149 999 
        # class 4   150 000 - 199 999 
        # class 5   200 000 - 499 999
        # class 6   >= 500 000 
        if y < 50000:
            return 1
        elif 50000 <= y <= 99999:
            return 2
        elif 100000 <= y <= 149999:
            return 3
        elif 150000 <= y <= 199999:
            return 4
        elif 200000 <= y <= 499999:
            return 5
        else:
            return 6

    def calculate_k(self, k=0):
        if (k == 0):
            self.k = math.ceil(math.sqrt(self.m_samples))
        else:
            self.k = math.ceil(k)

    def calculate_distances(self, sample):
        self.euclidean_distances = []
        self.manhattan_distances = []

        for m in range (0, self.m_samples):
            euclidean_distance = 0
            manhattan_distance = 0

            for n in range(0, self.n_features):
                # print(self.X[n][m])
                # print(sample)
                euclidean_distance += (self.X[n][m] - float(sample[n])) ** 2
                manhattan_distance += abs(self.X[n][m] - float(sample[n]))

            bisect.insort(self.euclidean_distances, (math.sqrt(euclidean_distance), self.Y[m]))
            bisect.insort(self.manhattan_distances, (manhattan_distance, self.Y[m]))

    def predict_euclidean(self):
        classes = np.array([dist[1] for dist in self.euclidean_distances[0:self.k]])
        print([dist[1] for dist in self.euclidean_distances[0:self.k]])
        class_value = np.bincount(classes).argmax()
        print(class_value)
        return self.class_value(class_value)

    def predict_manhattan(self):
        classes = np.array([dist[1] for dist in self.manhattan_distances[0:self.k]])
        print([dist[1] for dist in self.manhattan_distances[0:self.k]])
        class_value = np.bincount(classes).argmax()
        print(class_value)
        return self.class_value(class_value)
    
    def class_value(self, class_value):
        if class_value == 1:
            return "under 50.000,00 €"
        elif class_value == 2:
            return "between 50.000,00 € and 99.999,00 €"
        elif class_value == 3:
            return "between 100.000,00 € and 149.999,00 €"
        elif class_value == 4:
            return "between 150.000,00 € and 199.999,00 €"
        elif class_value == 5:
            return "between 200.000,00 € and 499.999,00 €"
        elif class_value == 6:
            return "over 500.000,00 €"