🏥 Healthcare Dataset – Migration vers MongoDB avec Docker

Ce projet a pour objectif de :

- Migrer un dataset CSV vers MongoDB
- Conteneuriser l’ensemble avec Docker
- Orchestrer MongoDB + script d’import via docker-compose

L’idée est d’avoir un pipeline simple :

CSV → Pandas → MongoDB
le tout exécuté automatiquement au démarrage des conteneurs.

----------------------------------------------------------------------------------------------

🚀 Migration des données vers MongoDB

La migration est réalisée via le script Python import_dataset_MongoDB.py.

Étapes principales du script

- Lecture du CSV avec Pandas
- Nettoyage / typage des colonnes :
- Dates (Date of Admission, Discharge Date)
- Numériques (Billing Amount, Age, Room Number)
- Conversion du DataFrame en documents MongoDB
- Connexion à MongoDB via pymongo
- Vidage de la collection cible
- Insertion complète des données

Extrait logique :

Le CSV est chargé depuis ./data/healthcare_dataset.csv

Les données sont insérées dans :

- Base : healthcare
- Collection : dataset

La collection est purgée avant chaque import pour garantir un état propre.

----------------------------------------------------------------------------------------------

📦 Dépendances Python

Elles sont centralisées dans requirements.txt :

- pandas
- pymongo
- numpy

Elles sont installées automatiquement lors du build Docker

----------------------------------------------------------------------------------------------

🐳 Dockerfile

Le Dockerfile sert à construire l’image Python chargée de l’import :

Logique globale :

- Image de base Python
- Copie du projet dans le conteneur
- Installation des dépendances (requirements.txt)
- Exécution du script import_dataset_MongoDB.py

Concrètement :

- Le conteneur démarre
- Lance immédiatement le script
- Insère les données dans MongoDB
- Puis s’arrête

----------------------------------------------------------------------------------------------

🧩 docker-compose

docker-compose.yml orchestre deux services :

🗄 MongoDB

- Image officielle Mongo
- Authentification activée
- Expose le port 27017
- Utilise un volume Docker pour persister les données


🐍 App Python (import)

- Build à partir du Dockerfile
- Dépend du service MongoDB
- Lance automatiquement l’import du CSV
- S’arrête une fois terminé
- Grâce à depends_on, MongoDB démarre avant le script d’import.

----------------------------------------------------------------------------------------------

▶️ Lancement du projet

À la racine :

- Pour lancer le conteneur et créer les images :
    --> docker-compose up --build

- Pour lancer le conteneur avec les images existantes :
    --> docker-compose up (-d pour lancer en arrière-plan)

Résultat :

- MongoDB démarre
- Le conteneur Python s’exécute
- Le dataset est injecté
- Le conteneur Python s’arrête
- MongoDB reste actif avec les données chargées

----------------------------------------------------------------------------------------------

🔍 Connexion MongoDB

Une fois lancé :

- Accéder au conteneur mongodb
    --> docker exec -it mongodb bash

- Se connecter à MongoDB via les ID 
    -- > mongosh -u root -p example --authenticationDatabase admin

- Charger la base de données "healthcare"
    --> use healthcare

Base : healthcare
Collection : dataset

- Ici nous pouvons exécuter des commandes mongo, exemples :
    --> db.dataset.countDocuments()
    --> db.dataset.find().limit(5).pretty()