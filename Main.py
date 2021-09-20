# Import nécessaire
from pymongo import MongoClient
import pymongo
import requests

#Connexion à la base mongo
ConnectionString = "mongodb+srv://Admin:CharlesLeBG@velo.sudxu.mongodb.net/Station?retryWrites=true&w=majority"
myClient = MongoClient(ConnectionString)

#Initialisation des collections
myDB=myClient['Station']

lille_collection=myClient['Lille']
paris_collection=myClient['Paris']
rennes_collection=myClient['Rennes']
lyon_collection=myClient['Lyon']

#Récupération des données des stations par ville

#LILLE

#Récupération de l'API
url="https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=-1&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"

reponse = requests.get(url)
contenu=reponse.json()
infos_stations=contenu['records']
print(len(infos_stations))
print(infos_stations[0])
