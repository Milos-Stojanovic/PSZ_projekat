import mysql.connector
import random
import math
import numpy as np
from sklearn.linear_model import LinearRegression, SGDRegressor
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import geocoder
import re
import csv
import pandas as pd

class LinearRegressionModel:

    def __init__(self, learning_rate=0.01, epochs=1000, test_size = 0.2):
        self.distances = {}
        self.unsuccessfulLocationCalculations = []
        self.counter = 0
        self.initialize_all_features()
        self.get_data_from_database(False)
        self.test_size = test_size
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.weight_params = None
        self.w0 = None
        self.cost_history = None
        


    def get_data_from_database(self, yes):
        if yes:
            self.create_connection()
            self.get_all_needed_data_from_database()


    def initialize_all_features(self):
        self.y = []
        self.udaljenostOdCentra = []
        self.kvadraturaNekretnine = []
        # self.tipNekretnine = []
        self.brojSoba = []
        self.spratnost = []
        # self.brojKupatila = []
        # self.uknjizeno = []
        # self.imaParking = []
        # self.imaLift = []
        # self.imaTerasu = []
        # self.imaBalkon = []
        # self.imaKamera = []
        # self.imaAlarm = []
        # self.imaVideoNadzorInterfon = []
        # self.imaInternet = []
        # self.imaTelefon = []
        # self.povrsinaZemljista = []

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

        other_location_name = self.split_on_uppercase(lokacija)
        # check dictionary hash
        self.counter += 1
        if self.counter % 10 == 0:
            print(self.counter)
        if other_location_name in self.distances:
            return self.distances[other_location_name]
        
        city_center_name = "Belgrade, Serbia"
        city_center_coordinates = self.get_location_coordinates(city_center_name)
        #print(self.split_on_uppercase(lokacija))
        other_location_coordinates = self.get_location_coordinates(other_location_name)

        distance = None;

        if city_center_coordinates and other_location_coordinates:
            distance = self.calculate_distance(city_center_coordinates, other_location_coordinates)
            # put distance for that location in dictionary hash
            self.distances[other_location_name] = distance
            #print(self.distances)


        return distance

    def split_on_uppercase(self, input_string):
        if input_string == "Beogradnavodi":
            return "Beograd na vodi"
        if input_string.lower() == "bulevarkr.aleksandra":
            return "Bulevar kralja Aleksandra"
        if input_string.lower() == "đerampijaca":
            return "Đeram pijaca"
        if input_string.lower() == "crvenikrst":
            return "Crveni Krst"
        if input_string.lower() == "vukovspomenik":
            return "Vukov spomenik"
        if input_string.lower() == "cvetkovapijaca":
            return "Cvetkova pijaca"
        if input_string.lower() == "južnibulevar":
            return "Južni bulevar"
        if input_string.lower() == "starigrad":
            return "Stari grad, Beograd"
        if input_string.lower() == "savskivenac":
            return "Savski venac"
        if input_string.lower() == "zelenivenac":
            return "Zeleni venac"
        if input_string.lower() == "kalenićpijaca":
            return "Kalenić pijaca"
        if input_string.lower() == "lion":
            return "Lion, Beograd"
        if input_string.lower() == "ledine":
            return "Ledine, Beograd"
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
        

        self.curr.execute("""
            select cenaNekretnine, kvadraturaNekretnine, tipNekretnine, brojSoba, brojKupatila, 
                uknjizeno, imaParking, imaLift, imaTerasu, imaBalkon, imaKamera,
                imaAlarm, imaVideoNadzorInterfon, imaInternet, imaTelefon, spratnost, lokacijaDeoGrada
            from nekretnine.nekretnine_db_zad2
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
            or lokacijaDeoGrada like '%Kalenićpijaca%')
                and brojSoba > 0 and spratnost is not null and tipNekretnine like 'stan';
        """)

        data = self.curr.fetchall()
        for row in data:
            distance = self.calculateDistance(row[16])
            if distance != None and distance < 40000 and round(float(row[1])) > 10:
                self.y.append(round(float(row[0])))
                self.kvadraturaNekretnine.append(round(float(row[1])))
                self.brojSoba.append(row[3])
                self.spratnost.append(row[15])
                self.udaljenostOdCentra.append(round(distance))

                
        # write data extracted from database to file (data.csv)
        self.write_data_to_file()

        # Combine features into one list
        self.features = list(zip(
            self.kvadraturaNekretnine,
            self.brojSoba,
            self.spratnost,
            self.udaljenostOdCentra
        ))

    def write_data_to_file(self):
        with open("data.csv", mode="w", newline='') as file:

            # Create a CSV writer object
            csv_writer = csv.writer(file)
            csv_writer.writerow(["distance","size","num_of_rooms","floor","price"])
        
            # Write each sublist as a row in the CSV file
            csv_writer.writerows(list(zip(
                self.udaljenostOdCentra,
                self.kvadraturaNekretnine,
                self.brojSoba,
                self.spratnost,
                self.y
            )))
    
    def normalize(self, x, x_min, x_max):
        #return ((x - x_min) * 2) / (x_max - x_min) - 1  # normalizacija na -1 do 1
        return (x - x_min) / (x_max - x_min) # normalizacija na 0 do 1
    
    def un_normalize(self, x, x_min, x_max):
        #return (x + 1) * (x_max - x_min) / 2 + x_min  # denormalizacija sa -1 do 1
        return x * (x_max - x_min) + x_min  # denormalizacija sa 0 do 1
    
    def fit(self, X, Y):
        n_samples, n_features = len(X), len(X.columns)
        print(n_samples)
        print(n_features)
        self.cost_history = []

        self.w0 = 0.0
        self.weight_params = np.zeros(n_features)

        print(np.sum(Y)/len(Y))
        
        for epoch in range(self.epochs):
            if epoch % 1000 == 0:
                print(f'Epoch {epoch}')
                print(str(self.w0) + " " + str(self.weight_params))


            hypothesis = np.dot(X, self.weight_params) + self.w0

            temp_w0 = self.w0 - self.learning_rate * (1 / n_samples) * np.sum(hypothesis - Y)
            temp_weight_params = self.weight_params - self.learning_rate * (1 / n_samples) * np.dot((hypothesis - Y), X)

            self.w0 = temp_w0
            self.weight_params = temp_weight_params
            

        

    def split_data_set(self, df, test_size=0.2):
        # random order in data set
        shuffle_df = df.sample(frac=1)

        # define a size for training set
        train_size = int((1 - test_size) * len(df))

        # split dataset
        train_set = shuffle_df[:train_size]
        test_set = shuffle_df[train_size:]

        return train_set, test_set


    def predict(self, test):
        return self.w0 + np.dot(test, self.weight_params)

    def predict_output_value(self, x):
        if self.weight_params is None:
            raise ValueError("The model has not been trained yet.")
        
        X = pd.DataFrame(x).min()
        X = self.normalize(X, self.X_min, self.X_max)
        prediction_of_input = self.predict(X)
        prediction = self.un_normalize(prediction_of_input, self.Y_min, self.Y_max)
        return prediction

    def root_mean_squared_error(self, y_true, y_pred):
        y_true = list(y_true)
        val = [(true - pred) ** 2 for true, pred in zip(y_true, y_pred)]
        return math.sqrt(sum(val) / len(val))
    

    def perform_linear_regression(self):
        df = pd.read_csv('data.csv')

        Y = df['price'].astype(float)
        self.Y_min = np.amin(Y)
        self.Y_max = np.amax(Y)

        X = df[['distance', 'size', 'num_of_rooms', 'floor']].astype(float)
        self.X_min = np.amin(X)
        self.X_max = np.amax(X)


        # divide data to test and train sets, normalize the data 
        df_train, df_test = self.split_data_set(df, test_size=0.2)

        Y_train = self.normalize(df_train['price'].astype(float), self.Y_min, self.Y_max)
        Y_test = self.normalize(df_test['price'].astype(float), self.Y_min, self.Y_max)

        X_train = self.normalize(
            df_train[['distance', 'size', 'num_of_rooms', 'floor']].astype(float),
            self.X_min, self.X_max)
        X_test = self.normalize(
            df_test[['distance', 'size', 'num_of_rooms', 'floor']].astype(float),
            self.X_min, self.X_max)

        self.fit(X_train, Y_train)
        

        # Evaluate the model on the test set and compare with train set
        Y_train_predictions = self.predict(X_train)
        Y_test_predictions = self.predict(X_test)

        Y_train_predictions = self.un_normalize(Y_train_predictions, self.Y_min, self.Y_max)
        Y_test_predictions = self.un_normalize(Y_test_predictions, self.Y_min, self.Y_max)

        Y_train_real = self.un_normalize(Y_train, self.Y_min, self.Y_max)
        Y_test_real = self.un_normalize(Y_test, self.Y_min, self.Y_max)
        print(Y_train_predictions)
        print(Y_train_real)

        rmse_train = self.root_mean_squared_error(Y_train_real, Y_train_predictions)
        rmse_test = self.root_mean_squared_error(Y_test_real, Y_test_predictions)
        print("INFO RMSE training data set:", rmse_train)
        print("INFO RMSE testing data set:", rmse_test)



if __name__ == "__main__":
   
    # MOJA IMPLEMENTACIJA
    sgd = LinearRegressionModel(learning_rate=0.01, epochs=25000, test_size=0.15)
    sgd.perform_linear_regression()

    # Print the optimized coefficients and cost history
    print("MINE Optimized Coefficients:", sgd.w0, sgd.weight_params)
    #print("MINE Cost History:", sgd.cost_history)

    # Make predictions
    y_pred = sgd.predict_output_value(dict(distance=[4068], size=[106], num_of_rooms=[3], floor=[10]))
    print("MINE Predicted Output:", y_pred)
    # X_test = [[130, 1, 5, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1]]
    # y_pred = sgd.predict(X_test)
    # print("MINE Predicted Output:", y_pred)
    print("MINE Coefficients:", sgd.w0, sgd.weight_params)

    