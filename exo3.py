# Import nécessaire
from pymongo import GEO2D, GEOSPHERE, MongoClient
from bson.son import SON
import pymongo
from pymongo.message import query
import requests

#Connexion à la base mongo
ConnectionString = "localhost:27017"
myClient = MongoClient(ConnectionString)

#Initialisation des collections
myDB=myClient['Station']

exo1_collection=myDB['Exo1']
# exo1_collection.create_index([("location",GEOSPHERE)])

# lat = input("Entrer votre latitude:")
# lon = input("Entrer votre longitude:")

query = {"location":{"$near": { "$geometry": {"type":"Point", "coordinates":[45.6,2.343]}}}}

for doc in exo1_collection.find(query).limit(3):
    print(doc)