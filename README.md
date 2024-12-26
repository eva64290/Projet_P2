# Projet de scraping du site Books to Scrape avec Openclassrooms

Ce projet extrait les données de tous les livres du site Books to Scrape.

## Installation

1. Clonez ce repository (https://github.com/eva64290/Projet_P2.git)
2. Créez un environnement virtuel : `python3 -m venv env`
3. Activez l'environnement virtuel :
   - Windows : `venv\Scripts\activate`
   - macOS/Linux : `source env/bin/activate`
4. Installez les dépendances : `pip install -r requirements.txt`

## Utilisation

Exécutez le script avec la commande : `python3 scraper.py`

Les données seront sauvegardées dans le fichier data avec pour chaque catégorie un fichier .csv correspondant. `
Les images en lien avec les livres de chaque catégorie seront téléchargés dans le fichier images.

Le développeur pourra suivre le traitement par catégorie et le nombre de livres extraits.

Une fois tout le site traité, un messaga apparait :'Scraping terminé. Les données ont été sauvegardées dans le dossier 'data' et les images dans le dossier 'images'.'

