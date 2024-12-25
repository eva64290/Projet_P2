import requests
from bs4 import BeautifulSoup
import csv
import os
from urllib.parse import urljoin

# URL de base du site à scraper
URL_BASE = 'http://books.toscrape.com/'

## Phase 1 : Extraction des informations détaillées d'un livre
def extraire_infos_livre(url):
    try:
        # Envoi de la requête HTTP et récupération du contenu de la page
        reponse = requests.get(url)
        reponse.raise_for_status()
        soup = BeautifulSoup(reponse.content, 'html.parser')
        
        # Extraction des différentes informations du livre
        titre = soup.find('h1').text
        prix = soup.find('p', class_='price_color').text
        disponibilite = soup.find('p', class_='instock availability').text.strip()
        description = soup.find('div', id='product_description')
        description = description.find_next_sibling('p').text if description else "Pas de description"
        categorie = soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip()
        note = len(soup.find('p', class_='star-rating').get('class')[1])
        image_url = urljoin(URL_BASE, soup.find('img')['src'])
        
        # Retour des informations sous forme de dictionnaire
        return {
            'titre': titre,
            'prix': prix,
            'disponibilite': disponibilite,
            'description': description,
            'categorie': categorie,
            'note': note,
            'image_url': image_url,
            'url': url
        }
    except requests.RequestException as e:
        print(f"Erreur lors de l'extraction des infos du livre {url}: {e}")
        return None

## Phase 2 : Extraction de tous les livres d'une catégorie
def extraire_livres_categorie(url_categorie):
    livres = []
    while url_categorie:
        try:
            # Envoi de la requête HTTP et récupération du contenu de la page
            reponse = requests.get(url_categorie)
            reponse.raise_for_status()
            soup = BeautifulSoup(reponse.content, 'html.parser')
            
            # Extraction des informations de chaque livre sur la page
            for article in soup.find_all('article', class_='product_pod'):
                url_livre = urljoin(url_categorie, article.find('a')['href'])
                infos_livre = extraire_infos_livre(url_livre)
                if infos_livre:
                    livres.append(infos_livre)
            
            # Gestion de la pagination
            suivant = soup.find('li', class_='next')
            url_categorie = urljoin(url_categorie, suivant.find('a')['href']) if suivant else None
        except requests.RequestException as e:
            print(f"Erreur lors de l'extraction de la catégorie {url_categorie}: {e}")
            break
    
    return livres

## Phase 3 : Téléchargement des images
def telecharger_image(url, chemin):
    try:
        # Envoi de la requête HTTP et sauvegarde du contenu de l'image
        reponse = requests.get(url)
        reponse.raise_for_status()
        with open(chemin, 'wb') as fichier:
            fichier.write(reponse.content)
    except requests.RequestException as e:
        print(f"Erreur lors du téléchargement de l'image {url}: {e}")

## Phase 4 : Sauvegarde des données dans un fichier CSV
def sauvegarder_csv(livres, nom_fichier):
    with open(nom_fichier, 'w', newline='', encoding='utf-8') as fichier:
        writer = csv.DictWriter(fichier, fieldnames=['titre', 'prix', 'disponibilite', 'description', 'categorie', 'note', 'image_url', 'url'])
        writer.writeheader()
        for livre in livres:
            writer.writerow(livre)

## Phase 5 : Extraction de toutes les catégories
def extraire_categories():
    try:
        # Envoi de la requête HTTP et récupération du contenu de la page d'accueil
        reponse = requests.get(URL_BASE)
        reponse.raise_for_status()
        soup = BeautifulSoup(reponse.content, 'html.parser')
        # Extraction des URLs de toutes les catégories
        return [urljoin(URL_BASE, a['href']) for a in soup.select('.nav-list ul a')]
    except requests.RequestException as e:
        print(f"Erreur lors de l'extraction des catégories: {e}")
        return []

## Phase 6 : Exécution principale
def main():
    # Création des dossiers pour stocker les données et les images
    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.exists('images'):
        os.makedirs('images')

    # Extraction de toutes les catégories
    categories = extraire_categories()
    
    # Pour chaque catégorie, extraction des livres et sauvegarde des données
    for url_categorie in categories:
        livres = extraire_livres_categorie(url_categorie)
        if livres:
            nom_categorie = livres[0]['categorie']
            nom_fichier = f"data/{nom_categorie.replace(' ', '_').lower()}.csv"
            sauvegarder_csv(livres, nom_fichier)
            
            # Téléchargement des images de chaque livre
            for livre in livres:
                nom_image = f"images/{livre['titre'].replace('/', '_')[:50]}.jpg"
                telecharger_image(livre['image_url'], nom_image)
            
            print(f"Catégorie '{nom_categorie}' traitée : {len(livres)} livres extraits")

    print("Scraping terminé. Les données ont été sauvegardées dans le dossier 'data' et les images dans le dossier 'images'.")

if __name__ == '__main__':
    main()
