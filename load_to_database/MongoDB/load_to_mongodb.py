import os
import csv
from pymongo import MongoClient


DATABASE = 'ucl_2024' # Nombre de la base de datos
COLLECTION = 'day4' # Nombre de la coleccion


# Crea una instancia de MongoClient que se conecta al servidor de MongoDB que se encuentra en 'localhost' (la máquina local)
client = MongoClient('localhost', 27017)
# Accede a la base de datos. Si no existe, MongoDB la creará cuando se inserte algún dato en ella.
db = client[DATABASE]
# Accede a la colección dentro de la base de datos. 
# Si la colección no existe, MongoDB la creará cuando se inserte algún documento en ella.
collection = db[COLLECTION]

# File path
file_path = os.path.join('extraction', 'raw_data', COLLECTION)

for file_name in os.listdir(file_path):
    if file_name.endswith('.csv'):
        complete_path = os.path.join(file_path, file_name)
        print(f"Loading data from {file_name}")

    # Read and load data from CSV files
    with open(complete_path, newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = [row for row in csv_reader]

        # Insert data into collection
        if data:
            collection.insert_many(data)
            print(f"Data from {file_name} inserted successfully.")

print("Upload completed.")

# Close session
client.close()