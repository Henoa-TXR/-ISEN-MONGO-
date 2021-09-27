# Import nécessaire
from pymongo import MongoClient, GEOSPHERE
import pymongo
import requests

#Connexion à la base mongo
ConnectionString = "mongodb+srv://Admin:CharlesLeBG@velo.sudxu.mongodb.net/Station?retryWrites=true&w=majority"
myClient = MongoClient(ConnectionString)

#Initialisation des collections
myDB=myClient['Station']

exo1_collection=myDB['Exo1']
#test_col=myDB['nom']

#Suppression des données précédentes
exo1_collection.drop()
exo1_collection.create_index([("location",GEOSPHERE)])


#Récupération des données des stations par ville




# #               LILLE



#Récupération de l'API
url="https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=-1&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"

reponse = requests.get(url)
contenu=reponse.json()
infos_stations=contenu['records']

lilleTab1=[]
for input_station in infos_stations:
    input_tab=input_station["fields"]["localisation"]
    lilleTab1.append(input_tab)

#Récupération des données de l'api
lilleTab=[]
i=0
for input_station in infos_stations:
    input_json={"ville":"Lille","nomstation":input_station["fields"]["nom"],"nombrevelo":input_station["fields"]["nbvelosdispo"],"nombreplaces":input_station["fields"]["nbplacesdispo"],"etat":input_station["fields"]["etat"],"location":{"type":"Point", "coordinates":lilleTab1[i]}}
    lilleTab.append(input_json)
    i=i+1

#Ajout des données dans la BDD
exo1_collection.insert_many(lilleTab)



#                       PARIS



#Pour les vélos parisiens, nous avons besoin de 2 API différentes.
#La récupération des données se fera donc en 2 étapes

#Récupération de la première API (nom des stations, coordonnées)
url="https://velib-metropole-opendata.smoove.pro/opendata/Velib_Metropole/station_information.json"

reponse = requests.get(url)
contenu=reponse.json()
infos_stations1=contenu['data']['stations']

#Récupération de la deuxième API (nombre de vélos et de places disponibles)
url="https://velib-metropole-opendata.smoove.pro/opendata/Velib_Metropole/station_status.json"

reponse = requests.get(url)
contenu=reponse.json()
infos_stations2=contenu['data']['stations']

#Récupération des données spécifiques de la première api
parisTab1=[]
for input_station in infos_stations1:
    input_tab=[input_station["name"],input_station["lat"],input_station["lon"]]
    parisTab1.append(input_tab)

#Récupération des données spécifiques de la deuxième api
parisTab2=[]
for input_station in infos_stations2:
    if(input_station["is_renting"]==1):
        etat="EN SERVICE"
    else:
        etat="HORS SERVICE"
    input_tab=[input_station["num_bikes_available"],input_station["num_docks_available"],etat]
    parisTab2.append(input_tab)

#Concaténation des données provenant des 2 APIs
if(len(parisTab1)==len(parisTab2)):
    parisTab=[]
    for i in range (0,len(parisTab1)):
        input_json={"ville":"Paris","nomstation":parisTab1[i][0],"nombrevelo":parisTab2[i][0],"nombreplaces":parisTab2[i][1],"etat":parisTab2[i][2],"location":{"type":"Point", "coordinates":[parisTab1[i][1],parisTab1[i][2]]}}
        parisTab.append(input_json)
else:
    print("ERROR IN PARIS' API")

#Ajout des données dans la BDD
exo1_collection.insert_many(parisTab)



#               LYON


# Récupération de l'API
url="https://download.data.grandlyon.com/ws/rdata/jcd_jcdecaux.jcdvelov/all.json?compact=false"

reponse = requests.get(url)
contenu=reponse.json()
infos_stations=contenu['values']

# Récupération des données de l'api

lyonTab1=[]
for input_station in infos_stations:
    input_tab=[float(input_station["lat"]),float(input_station["lng"])]
    lyonTab1.append(input_tab)
i=0
lyonTab=[]
for input_station in infos_stations:
    if(input_station["status"]=="OPEN"):
        etat="EN SERVICE"
    else:
        etat="HORS SERVICE"
    input_json={"ville":"Lyon","nomstation":input_station["pole"],"nombrevelo":input_station["available_bikes"],"nombreplaces":input_station["available_bike_stands"],"etat":etat,"location":{"type":"Point", "coordinates":lyonTab1[i]}}
    lyonTab.append(input_json)
    i=i+1

# Ajout des données dans la BDD
exo1_collection.insert_many(lyonTab)




# #               Rennes



#Récupération de l'API
url="https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=etat-des-stations-le-velo-star-en-temps-reel&q=&rows=-1&facet=nom&facet=etat&facet=nombreemplacementsactuels&facet=nombreemplacementsdisponibles&facet=nombrevelosdisponibles"

reponse = requests.get(url)
contenu=reponse.json()
infos_stations=contenu['records']

#Récupération des données de l'api

rennesTab1=[]
for input_station in infos_stations:
    input_tab=input_station["fields"]["coordonnees"]
    rennesTab1.append(input_tab)

rennesTab=[]
i=0
for input_station in infos_stations:
    if(input_station["fields"]["etat"]=="En fonctionnement"):
        etat="EN SERVICE"
    else:
        etat="HORS SERVICE"
    input_json={"ville":"Rennes","nomstation":input_station["fields"]["nom"],"nombrevelo":input_station["fields"]["nombrevelosdisponibles"],"nombreplaces":input_station["fields"]["nombreemplacementsdisponibles"],"etat":etat,"location":{"type":"Point", "coordinates":rennesTab1[i]}}
    rennesTab.append(input_json)
    i=i+1

#Ajout des données dans la BDD
exo1_collection.insert_many(rennesTab)
