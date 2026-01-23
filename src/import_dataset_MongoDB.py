#!/usr/bin/env python
# coding: utf-8


import pandas as pd

from pymongo import MongoClient



df = pd.read_csv('./data/healthcare_dataset.csv')



df['Date of Admission'] = pd.to_datetime(df['Date of Admission'])
df['Discharge Date'] = pd.to_datetime(df['Discharge Date'])

df['Billing Amount'] = df['Billing Amount'].astype(float)

df['Age'] = df['Age'].astype(int)
df['Room Number'] = df['Room Number'].astype(int)



# Transforme en document
data = df.to_dict('records')



client = MongoClient(
    "mongodb://root:example@mongodb:27017/",
    authSource="admin"
)
db = client['healthcare']  # base de données
collection = db['dataset']  # collection


# Vider la collection avant insertion
collection.delete_many({})
print(f"Collection vidée. Nombre de documents avant insertion : {collection.count_documents({})}")

# Insérer les données depuis le CSV
data = df.to_dict('records')
collection.insert_many(data)
print(f"{len(data)} documents insérés dans MongoDB.")

exit(0)  # Termine le script et arrête le conteneur