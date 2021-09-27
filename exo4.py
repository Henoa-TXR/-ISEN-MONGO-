# Import nécessaire
from pymongo import MongoClient, GEOSPHERE
import pymongo
import requests
import sys

#Connexion à la base mongo
ConnectionString = "mongodb+srv://Admin:CharlesLeBG@velo.sudxu.mongodb.net/Station?retryWrites=true&w=majority"
myClient = MongoClient(ConnectionString)

#Initialisation des collections
myDB=myClient['Station']

exo4_collection=myDB['Exo4']

end=False

while (end==False):

    goodInput=False

    while (goodInput==False):
        print("")
        print("Programme de gestion des vélos en libre service.")
        print("Veuillez sélectionner votre ville : ")
        print("(1) Lille")
        print("(2) Paris")
        print("(3) Lyon")
        print("(4) Rennes")
        print("(0) Terminer la session")

        numeroVille = input("Entrez le numéro correspondant : ")

        if (numeroVille=="1" or numeroVille=="2" or numeroVille=="3" or numeroVille=="4"):
            goodInput=True
        elif (numeroVille=="0"):
            sys.exit()
        else:
            print("Erreur de saisie : merci d'entrer le numéro de la ville souhaitée.")

    city=""
    if (numeroVille=="1"):
        city="Lille"
    elif (numeroVille=="2"):
        city="Paris"
    elif (numeroVille=="3"):
        city="Lyon"
    else:
        city="Rennes"

    

    endVille=False
    while (endVille==False):
        print()
        print("Gestion des vélos de la ville de " + city + ".")

        goodInput2=False
        while (goodInput2==False):
            print("")
            
            print("Que désirez vous faire ?")
            print("(1) Rechercher une station")
            print("(2) Connaitre toutes les stations avec moins de 20 pourcents de vélos disponibles")
            print("(0) Quitter la gestion des vélos de la ville de " + city + " et revenir au menu principal")

            choix=input("Entrez le numéro correspondant à la fonction désirée : ")

            if (choix=="1" or choix=="2"):
                goodInput2=True
            elif (choix=="0"):
                goodInput2=True
                endVille=True
            else:
                print("Erreur de saisie : merci d'entrer une commande existante.")

        if (choix=="1"):
            endRecherche=False
            while (endRecherche==False):
                print()
                print("Rechercher une station.")
                rechercheVille=input("Entrer une partie du nom de la station recherchée, ou bien tapez 0 pour sortir :")
                if (rechercheVille=="0"):
                    endRecherche=True
                else:
                    queryname={"ville":city,"nomstation": {"$regex":rechercheVille, "$options":"i"}}
                    stations=exo4_collection.find(queryname)
                    i=0
                    for station in stations:
                        i=i+1
                        print(station)
                    if (i>1):
                        print("Plusieurs stations trouvées. Veuillez affiner la rechercher si vous souhaitez opérer des modifications.")
                    elif (i==0):
                        print("Pas de station trouvée : merci de réitérer la recherche.")
                    else:
                        goodInput3=False
                        while (goodInput3==False):
                            print("Souhaitez vous mettre à jour (1), supprimer (2) la station ou bien revenir à la recherche (0) ?")
                            choix2=input("Entrez le numéro correspondant à la fonction désirée : ")
                            if (choix2=="1" or choix2=="2"):
                                goodInput3=True
                            elif (choix2=="0"):
                                goodInput3=True
                            else:
                                print("Erreur de saisie : merci d'entrer une commande existante.")
                        if (choix2=="2"):
                            exo4_collection.delete_one({"ville":city, "nomstation":{"$regex":rechercheVille, "$options":"i"}})
                        elif (choix2=="1"):
                            print()
                            print("Veuillez entrer (1) pour modifier le nom ou (2) pour modifier l'état de la station. Pour annuler, entrez (0).")
                            choix3=input("Entrez le numéro correspondant à la fonction désirée : ")
                            if (choix3=="1"):
                                print()
                                newname=input("Merci d'entrer le nouveau nom : ")
                                myquery={"ville":city,"nomstation":{"$regex":rechercheVille, "$options":"i"}}
                                newvalues={ "$set": { "nomstation": newname } }
                                exo4_collection.update_one(myquery,newvalues)
                            elif (choix3=="2"):
                                print()
                                newetat=input("Merci d'entrer l'état actuel de la station, (1) pour EN SERVICE et (2) pour HORS SERVICE :")
                                myquery={"ville":city,"nomstation":{"$regex":rechercheVille, "$options":"i"}}
                                etatstation=""
                                if(newetat=="1"):
                                    newvalues={ "$set": { "etat": "EN SERVICE" } }
                                    exo4_collection.update_one(myquery,newvalues)
                                    print("Modifications effectuées.")
                                elif(newetat=="2"):
                                    newvalues={ "$set": { "etat": "HORS SERVICE" } }
                                    exo4_collection.update_one(myquery,newvalues)
                                    print("Modifications effectuées.")
                            
        elif(choix=="2"):
            stationsUnder20prct=[]
            allCityStations=exo4_collection.find({"ville":city})
            for station in allCityStations:
                if (station["nombrevelo"]+station["nombreplaces"]!=0):
                    if (station["nombrevelo"]/(station["nombrevelo"]+station["nombreplaces"])<=0.2):
                        stationsUnder20prct.append(station)
            
            for station in stationsUnder20prct:
                print(station)


                            
                            

        

    


