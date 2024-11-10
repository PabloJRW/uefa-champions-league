import os
import pandas as pd
from pymongo import MongoClient


DATABASE = 'ucl_2024' # Nombre de la base de datos
COLLECTION = 'day4' # Nombre de la coleccion


# Crea una instancia de MongoClient que se conecta al servidor de MongoDB que se encuentra en 'localhost' (la máquina local)
client = MongoClient('localhost', 27017)
# Accede a la base de datos llamada 'supertienda'. Si no existe, MongoDB la creará cuando se inserte algún dato en ella.
db = client[DATABASE]
# Accede a la colección llamada 'ordenes' dentro de la base de datos 'supertienda'. 
# Si la colección no existe, MongoDB la creará cuando se inserte algún documento en ella.
col = db[COLLECTION]

# Ruta del archivo CSV
FILE_PATH = os.path.join('data','raw','Encuentra24','autos_usados.csv')

# Carga del archivo CSV a Pandas
try:
    df = pd.read_csv(FILE_PATH, encoding="latin-1")
except FileNotFoundError:
    print(f"El archivo no se encuentra en la ruta: {FILE_PATH}")


documents = []
for index, row in df.iterrows():
    document = {
       
    }
    documents.append(document)

# Insertar los documentos en la colección, evitando duplicados.
try: 
    if documents:  # Verifica que la lista de documentos no esté vacía
        for doc in documents:
            # Verificar si el documento ya existe basado en múltiples campos, por ejemplo, 'OrderID' y 'CustomerID'
            query = {
                
            }
            if col.count_documents(query) == 0:  # Si no existe ningún documento con esos campos
                col.insert_one(doc)  # Insertar el documento
        print("Documentos guardados correctamente...")

except Exception as e:
    print(f"Error al insertar documentos: {e}")