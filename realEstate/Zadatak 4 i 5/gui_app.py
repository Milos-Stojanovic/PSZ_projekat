import tkinter as tk
from zadatak_4_lin_reg import LinearRegressionModel
from zadatak_5_knn import KNN_Model

def select_model():
    selected_option = radio_var.get()
    if selected_option == "KNN":
        kNN_label1.config(state=tk.NORMAL)
        kNN_entry1.config(state=tk.NORMAL)
        radio_button_distance_1.config(state=tk.NORMAL)
        radio_button_distance_2.config(state=tk.NORMAL)
        #concat_button.config(bg="lightgray")
        #concat_button.config(fg="green")
    else:
        #concat_button.config(bg="red")
        kNN_label1.config(state=tk.DISABLED)
        kNN_entry1.config(state=tk.DISABLED)
        radio_button_distance_1.config(state=tk.DISABLED)
        radio_button_distance_2.config(state=tk.DISABLED)

def select_distance():
    return True
        

def determine_price():
    def is_valid_input(entry):
        try:
            value = int(entry.get())
            return value > 0
        except ValueError:
            return False

    if all(is_valid_input(entry) for entry in (entry1, entry2, entry3, entry4)):
        selected_option = radio_var.get()

        distance = int(entry1.get())
        size = int(entry2.get())
        num_of_rooms = int(entry3.get())
        floor = int(entry4.get())


        if selected_option == "LinReg":
            data = dict(distance=[distance], size=[size], num_of_rooms=[num_of_rooms], floor=[floor])
            print(data)
            price = lin_reg_model.predict_output_value(data)
            result_label.config(text="Predicted price: {} €".format(round(price, 2)), fg="green", font=("Helvetica", 14))

        if selected_option == "KNN":
            data = [distance, size, num_of_rooms, floor]
            print(data)
            selected_distance = distance_type.get()
            if(kNN_entry1.get() != None and is_valid_input(kNN_entry1)):
                knn_model.calculate_k(int(kNN_entry1.get()))
                print(knn_model.k)

            if (kNN_entry1.get() == ""):
                knn_model.calculate_k()

            knn_model.calculate_distances(data)

            if selected_distance == "Euclidean":
                price = knn_model.predict_euclidean()
                result_label.config(text="Predicted price:\n {}".format(price), fg="green", font=("Helvetica", 14))

            elif selected_distance == "Manhattan":
                price = knn_model.predict_manhattan()
                result_label.config(text="Predicted price:\n {}".format(price), fg="green", font=("Helvetica", 14))

            
    else:
        result_label.config(text="Invalid Input, Please enter valid values!", fg="red", font=("Helvetica", 14))

# Create the main window
window = tk.Tk()
window.title("Belgrade - flat purchase price calculator")
window.geometry("500x500")  # Set default width and height
# Create labels
label1 = tk.Label(window, text="Distance from city center (m):", font=("Helvetica", 12))
label2 = tk.Label(window, text="Flat size (m²):", font=("Helvetica", 12))
label3 = tk.Label(window, text="Number of rooms:", font=("Helvetica", 12))
label4 = tk.Label(window, text="Floor:", font=("Helvetica", 12))

# Create four textboxes
entry1 = tk.Entry(window, width=20, font=("Helvetica", 12))
entry2 = tk.Entry(window, width=20, font=("Helvetica", 12))
entry3 = tk.Entry(window, width=20, font=("Helvetica", 12))
entry4 = tk.Entry(window, width=20, font=("Helvetica", 12))

# Create a button to trigger concatenation
concat_button = tk.Button(window, text="Determine price", command=determine_price, font=("Helvetica", 12))

# Create labels to display the concatenated text and error messages
result_label = tk.Label(window, text="", fg="green", font=("Helvetica", 14))
error_label = tk.Label(window, text="", fg="red", font=("Helvetica", 14))

# Create radio buttons
radio_var = tk.StringVar()
radio_button1 = tk.Radiobutton(window, text="Linear regression", variable=radio_var, value="LinReg", font=("Helvetica", 12), command=select_model)
radio_button2 = tk.Radiobutton(window, text="KNN", variable=radio_var, value="KNN", font=("Helvetica", 12), command=select_model)
radio_var.set("LinReg")






# Create a frame to encapsulate the kNN variables - K and types of distances
input_frame = tk.Frame(window)
kNN_label1 = tk.Label(input_frame, text="Value of K (auto-determined if empty):", font=("Helvetica", 10))
kNN_entry1 = tk.Entry(input_frame, width=20, font=("Helvetica", 12))

# Create radio buttons for types of distances
distance_type = tk.StringVar()
radio_button_distance_1 = tk.Radiobutton(input_frame, text="Euclidean", variable=distance_type, value="Euclidean", font=("Helvetica", 12), command=select_distance)
radio_button_distance_2 = tk.Radiobutton(input_frame, text="Manhattan", variable=distance_type, value="Manhattan", font=("Helvetica", 12), command=select_distance)
distance_type.set("Euclidean")





# Arrange widgets in a grid layout with consistent padding

radio_button1.grid(row=0, column=0, pady=(25, 10), padx=25,  sticky="w")
label1.grid(row=1, column=0, pady=(30, 10), padx=30, sticky="w")
label2.grid(row=2, column=0, pady=10, padx=30, sticky="w")
label3.grid(row=3, column=0, pady=10, padx=30, sticky="w")
label4.grid(row=4, column=0, pady=10, padx=30, sticky="w")

radio_button2.grid(row=0, column=1, pady=(25, 10), padx=45, sticky="w")
entry1.grid(row=1, column=1, pady=(30, 10), padx=0)
entry2.grid(row=2, column=1, pady=10, padx=0)
entry3.grid(row=3, column=1, pady=10, padx=0)
entry4.grid(row=4, column=1, pady=10, padx=0)

# Add the input frame
input_frame.grid(row=5, column=0, columnspan=2, pady=5, padx=10, sticky="w")

# Add labels and entries to the input frame
kNN_label1.grid(row=0, column=0, pady=5, padx=10, sticky="w")
radio_button_distance_1.grid(row=1, column=0, pady=5, padx=10)
kNN_entry1.grid(row=0, column=1, pady=5, padx=10)
radio_button_distance_2.grid(row=1, column=1, pady=5, padx=10)
select_model()

concat_button.grid(row=6, column=0, pady=10, columnspan=2)
result_label.grid(row=7, column=0, pady=10, columnspan=2)

# train models
lin_reg_model = LinearRegressionModel(learning_rate=0.03, epochs=12000, test_size=0.15)
lin_reg_model.perform_linear_regression()
knn_model = KNN_Model()

# Start the main event loop
window.mainloop()