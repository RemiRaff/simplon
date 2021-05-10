#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  4 10:24:06 2021

@author: simplon
"""

# 11.2.Analyse_exploratoire.pdf
# données: 'fandango_scores.csv'
# FILM,RottenTomatoes,RottenTomatoes_User,Metacritic,Metacritic_User,IMDB,
# Fandango_Stars,Fandango_Ratingvalue,RT_norm,RT_user_norm,Metacritic_norm,
# Metacritic_user_nom,IMDB_norm,RT_norm_round,RT_user_norm_round,
# Metacritic_norm_round,Metacritic_user_norm_round,IMDB_norm_round,
# Metacritic_user_vote_count,IMDB_user_vote_count,Fandango_votes,
# Fandango_Difference

import pandas as pd

data = pd.read_csv("/home/simplon/Documents/Datas/fandango_scores.csv") # , index_col=[1] création de l'index

norm_reviews = data[['FILM', 'RT_user_norm', 'Metacritic_user_nom', 'IMDB_norm', 'Fandango_Ratingvalue', 'Fandango_Stars']]
# KeyError si [], [[]] retourne un DF
# print(norm_reviews.head())
#                              FILM  ...  Fandango_Stars
# 0  Avengers: Age of Ultron (2015)  ...             5.0
# 1               Cinderella (2015)  ...             5.0
# 2                  Ant-Man (2015)  ...             5.0
# 3          Do You Believe? (2015)  ...             5.0
# 4   Hot Tub Time Machine 2 (2015)  ...             3.5
# [5 rows x 6 columns]

norm_reviews.set_index('FILM',inplace=True) # sans KeyError sur loc
# print(norm_reviews.head())
#                                 RT_user_norm  ...  Fandango_Stars
# FILM                                          ...                
# Avengers: Age of Ultron (2015)           4.3  ...             5.0
# Cinderella (2015)                        4.0  ...             5.0
# Ant-Man (2015)                           4.5  ...             5.0
# Do You Believe? (2015)                   4.2  ...             5.0
# Hot Tub Time Machine 2 (2015)            1.4  ...             3.5

import matplotlib.pyplot as plt


## Barres Verticales
fig, ax = plt.subplots()

pos = range(1,6) # pour afficher les 5 colonnes

num_cols = ['RT_user_norm', 'Metacritic_user_nom', 'IMDB_norm', 'Fandango_Ratingvalue', 'Fandango_Stars']

bar_heights = norm_reviews[num_cols].loc['Avengers: Age of Ultron (2015)'].values
# KeyError 'Avengers: Age of Ultron (2015)', index_col pas définie dans read_csv

# bar_heights = norm_reviews[num_cols].iloc[0].values # 1er film
# print(norm_reviews.iloc[0].values) # ['Avengers: Age of Ultron (2015)' 4.3 3.55 3.9 4.5 5.0]

width = 0.5

ax.bar(pos, bar_heights, width)

ax.set_xticks(pos)
ax.set_xticklabels(num_cols,rotation=90)

ax.set_xlabel('Sources de notation')
ax.set_ylabel('Note moyenne')
ax.set_title('Moyenne des notes utilisateurs pour le film Avengers: Age of Ultron (2015)')

plt.show()
plt.close()
# Conclusion: Metecritic + sévère, Fandango mieux noté


# Barres Horizontales
fig, ax = plt.subplots()

ax.barh(pos, bar_heights, width)

ax.set_yticks(pos)
ax.set_yticklabels(num_cols)

ax.set_ylabel('Sources de notes')
ax.set_xlabel('Note moyenne')
ax.set_title("Note moyenne utilisateurs pour le film Avengers: Age of Ultron (2015)")

plt.show()
plt.close()
# Conclusion: même conclusion que précédemment


# Nuage de points
fig, ax = plt.subplots()

ax.scatter(norm_reviews['Fandango_Ratingvalue'],norm_reviews['RT_user_norm'])

ax.set_xlabel('Fandango')
ax.set_ylabel('Rotten Tomatoes')

plt.show()
plt.close()
# Conclusion:
#  * + de points en haut à droite donc pour un même film Fandango note mieux
#  * pour Fandango pas de note sous les 2 


# Intervertir les axes
fig = plt.figure(figsize=(10,4),dpi=200) # rajout du figsize pour chevauchement

ax1 = fig.add_subplot(1,2,1)
ax1.scatter(norm_reviews['Fandango_Ratingvalue'],norm_reviews['RT_user_norm'])
ax1.set_xlabel('Fandango')
ax1.set_ylabel('Rotten Tomatoes')

ax2 = fig.add_subplot(1,2,2)
ax2.scatter(norm_reviews['RT_user_norm'],norm_reviews['Fandango_Ratingvalue'])
ax2.set_ylabel('Fandango')
ax2.set_xlabel('Rotten Tomatoes')

plt.show()
plt.close()
# Conclusion:
#  * graph 1 comme précédemment
#  * graph 2 RT utilise les notes de 1 à 5, elles sont globalement + basses
# relation linéaire donc corrélation possible


# Comparaison de corrélations
fig = plt.figure(figsize=(12,5),dpi=200) # rajout du figsize pour chevauchement

ax1 = fig.add_subplot(1,3,1)
ax1.scatter(norm_reviews['Fandango_Ratingvalue'],norm_reviews['RT_user_norm'],color='r')
ax1.set_xlabel('Fandango')
ax1.set_ylabel('Rotten Tomatoes')
ax1.set_xlim(0,5)
ax1.set_ylim(0,5)

ax2 = fig.add_subplot(1,3,2)
ax2.scatter(norm_reviews['Fandango_Ratingvalue'],norm_reviews['Metacritic_user_nom'],color='orange')
ax2.set_xlabel('Fandango')
ax2.set_ylabel('Metacritic')
ax2.set_xlim(0,5)
ax2.set_ylim(0,5)

ax3 = fig.add_subplot(1,3,3)
ax3.scatter(norm_reviews['Fandango_Ratingvalue'],norm_reviews['IMDB_norm'],color='g')
ax3.set_xlabel('Fandango')
ax3.set_ylabel('IMDB')
ax3.set_xlim(0,5) # délimiter le graphique
ax3.set_ylim(0,5)

plt.show()
plt.close()
# Conclusion: comparaison de Fandango / aux 3 autres sites
#  * RT est le site le + sévère, plus de points groupés en bas vers y=1
#  * Metacritics et MDB n'ont presque pas de film noté au dessus de 4.5
#  * le nuage le plus groupé est le G3, les notes sont plus homogènes entre les
#    2 sites
# corrélation proportionnelle mais fandango a des notes + élévé
# print(norm_reviews.corr())


###############################################################
# Distribution de fréquences
###############################################################
# Pour connaitre le nb de notes données
imdb_distribution = norm_reviews['IMDB_norm'].value_counts().sort_index()
# sort_value faux, tri la mauvaise colonne
print(imdb_distribution)


fig, ax = plt.subplots()

ax.hist(norm_reviews['Fandango_Ratingvalue'], range=(0,5), bins=20) # bins=20 nb de classes default 10
ax.set_xlabel('Fandango')
ax.set_ylabel('Notes')
ax.set_title("Notes données par Fandango")

plt.show()
plt.close()
# Conclusion: les notes les plus données sont 4 et 4.5 et aucune à 2 ou moins


###############################################################
# Comparaison d'histogrammes
###############################################################
fig = plt.figure(figsize=(18,5)) # rajout du figsize pour chevauchement
# 16,5 sur 1 ligne

ax1 = fig.add_subplot(141) # 221 valeur pour 2x2
ax1.hist(norm_reviews['Fandango_Ratingvalue'], range=(0,5), bins=20) # range est la suite de valeurs à afficher
ax1.set_ylim(0,50)
ax1.set_xlabel('Fandango')
ax1.set_ylabel('Notes')
ax1.set_title("Notes données par Fandango")

ax2 = fig.add_subplot(142) # 222 valeur pour 2x2
ax2.hist(norm_reviews['RT_user_norm'], range=(0,5), bins=20)
ax2.set_ylim(0,50)
ax2.set_xlabel('Rotten Tomatoes')
ax2.set_ylabel('Notes')
ax2.set_title("Notes données par Rotten Tomatoes")

ax3 = fig.add_subplot(143) # 223 valeur pour 2x2
ax3.hist(norm_reviews['Metacritic_user_nom'], range=(0,5), bins=20)
ax3.set_ylim(0,50)
ax3.set_xlabel('Metacritic')
ax3.set_ylabel('Notes')
ax3.set_title("Notes données par Metacritic")

ax4 = fig.add_subplot(144) # 224 valeur pour 2x2
ax4.hist(norm_reviews['IMDB_norm'], range=(0,5), bins=20) # sélection de 20 classes avec bins
ax4.set_ylim(0,50)
ax4.set_xlabel('IMDB')
ax4.set_ylabel('Notes')
ax4.set_title("Notes données par IMDB") # subplot_adjust pour gérer les espaces sous grphique

plt.show()
plt.close()
# Concusion:
#   * 2 pics pour Fandango, à 3.5 et 4, notes sur plage de 2.5 à 5
#   * distribution plus homogène pour RT de 1 à 4.5, pas plus de 20 films par note
#   * Metacritics pointe centrée à 3.5, la moitié des films sont autour de cette pointe
#   * IMDB n'a pas de note sous 2, note groupée vers 3.5


#############################################################################
# Plusieurs diagrammes à boîtes
#############################################################################
fig, ax = plt.subplots() # crée et assigne les objets fig et ax

num_cols = ['RT_user_norm', 'Metacritic_user_nom', 'IMDB_norm', 'Fandango_Ratingvalue']

ax.boxplot([norm_reviews[num_cols[0]],norm_reviews[num_cols[1]],
            norm_reviews[num_cols[2]],norm_reviews[num_cols[3]]])
# showfliers=False

ax.set_xticklabels(num_cols, rotation=90) # 90 pour meilleure visibilité

ax.set_ylim(0,5)
ax.set_ylabel('Notes')
ax.set_title('Notation des sites')

plt.show()
plt.close()
# Conclusion:
#   * 3 sites (RT, Metacritics, IMDB) ont sesiblement la même médiane,
#     avec un léger retrait pour RT. Fandango a une médiane autour de 4.
#   * Min et Max plus groupé pour IMDB et Fangodango
# IMDB plus de outfliers
# RT: les quartiles sont assez espacés