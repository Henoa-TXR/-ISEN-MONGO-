# Import nécessaire
from pymongo import MongoClient
import pymongo

# Fonction qui permet de se connecter à la BDD "Station" de Mongo Atlas
def get_database():

    ConnectionString = "mongodb+srv://Admin:CharlesLeBG@velo.sudxu.mongodb.net/Station?retryWrites=true&w=majority"
    client = MongoClient(ConnectionString)

    return client['Station']


dbname = get_database()
print(list(dbname.nom.find()))