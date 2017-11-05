Le but de se projet est de répondre à certaines problématique de phonologie et de morphologie par l'intérmédiaire de python et des sciences statistiques.
Nos problématiques sont : 
Y a-t-il un lien entre le nombre de consones et le nombre de voyelle dans les langues ?
Y a-t-il des liens avec d'autres phénomènes phonologiques ? Ton, nasalisation ?
Y a-t-il des liens entre inventaire de sons et distribution géographique ?
Y a-t-il des liens entre inventaire de sons et la morphologie des langues ?

Pour répondre à cette problématique nous analysons un fichier csv : Data/language.csv

Ce fichier est analysable de deux manières:
-> Avec le programme parser.py dans Source/parser.py qui va créer un fichier description.txt dans le dossier Resultats/
   mais aussi des fichiers javascript dans le dossier Source/Map afin d'avoir des cartes interactives en HTML5 et js.
   Le programme possède différente options :
	-> --full afin de créer le fichier description.txt
	-> --desc en complément de --full afin que la description soit accompagné de toutes les valeurs possibles de chaque colonnes

   parser.py utilise principalement 2 fonctions :
	-> writeGeoJSON(dataframe, filename, columns_name)
		-> dataframe un dataframe
		-> filename le nom du fichier qui contiendra la variable js
		-> columns_name, une liste contenant le nom des colonnes à mettre dans la variable js en plus des colonnes Name, longitude et latitude
	   Cette fonction écrit une variable js dans un fichier filename avec les colonnes spécifié en propriété

	-> writePossible(dataframe, writePossible=False)
		-> dataframe un dataframe
		-> writePossible un booléen si Vrai, sera écrit aussi dans le fichier Resultats/description.txt les valeurs possibles pour chaque colonnes 
 	   Cette fonction créer un fichier txt détaillant les colonnes et les valeurs possible du dataframe

-> Avec le programme statistics.py qui va créer des images de graphiques au format .png pour nos problématiques. Ces graphiques sont créer dans le dossier 
   Resultats/. Le programme possède l'option :
	-> --show afin de montrer à l'écran chaque graphique ainsi créer en plus de les sauvegarder.

   statistics.py utilise principalement une fonction :
	-> compareColuns(dataframe, x_name, y_name, alt_x_name=None, alt_y_name=None, show=False)
		-> dataframe un dataframe
		-> x_name, le nom d'une colonnes à comparé
		-> y_name, le nom d'une colonnes comparante
		-> alt_x_name, le nom à afficher de la colonne x_name (x_name si None)
		-> alt_y_name, le nom à afficher de la colonne y_name (y_name si None)
		-> show, un booléen qui affiche plus de sauvegarder le graphique si égale à True
	   Cette fonction créer un graphique comparant deux colonnes selon le pourcentage de y pour chaque valeurs possible de x

Ce projet utilise les modules python suivants : 
 -> numpy 
 -> pandas 
 -> matplolib.pyplot 
 -> sys

Ce projet utilise git et github dont voici le lien : 
 -> https://github.com/GerardPalace/Phonologies.git

Mais aussi :
 -> Leaflet, an open-source JavaScript library for mobile-friendly interactive maps : http://leafletjs.com/
 -> Mapbox, An open source mapping platform for custom designed maps : https://www.mapbox.com/
 -> WALS Online, a large database of structural properties of languages gathered from descriptive materials : http://wals.info/