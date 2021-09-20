# Import nécessaire
from pymongo import MongoClient
import pymongo
import requests

#Connexion à la base mongo
ConnectionString = "mongodb+srv://Admin:CharlesLeBG@velo.sudxu.mongodb.net/Station?retryWrites=true&w=majority"
myClient = MongoClient(ConnectionString)

#Initialisation des collections
myDB=myClient['Station']

exo1_collection=myDB['Exo1']
test_col=myDB['nom']

#Récupération des données des stations par ville

#LILLE

#Récupération de l'API
url="https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=-1&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"

reponse = requests.get(url)
contenu=reponse.json()
infos_stations=contenu['records']

#Suppression des données précédentes
exo1_collection.drop()

#Récupération des données de l'api
tab=[]
for input_station in infos_stations:
    input_json={"ville":"Lille","nomstation":input_station["fields"]["nom"],"nombrevelo":input_station["fields"]["nbvelosdispo"],"nombreplaces":input_station["fields"]["nbplacesdispo"],"etat":input_station["fields"]["etat"],"latitude":input_station["fields"]["localisation"][0],"longitude":input_station["fields"]["localisation"][1]}
    tab.append(input_json)

#Ajout des données dans la BDD
exo1_collection.insert_many(tab)

