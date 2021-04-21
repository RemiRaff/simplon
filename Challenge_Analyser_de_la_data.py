#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 10:48:14 2021

@author: simplon
"""

# 8.2._Challenge

# Données:
# all-ages.csv
# recent-grads.csv

# https://pandas.pydata.org

import pandas as pd
import numpy as np


########################################################
#######                          Introduction au dataset
########################################################
all_ages = pd.read_csv("/home/simplon/all-ages.csv")
recent_grads = pd.read_csv("/home/simplon/recent-grads.csv")

# all_ages.head(5) # .head() affiche les 5 premiers par défaut
# Major_code   Major   Major_category   Total   Employed
# Employed_full_time_year_round   Unemployed   Unemployment_rate   Median   P25th   P75th

# recent_grads.head()
# 21 culumns


########################################################
#######        Nombre d'étudiants par catégorie de Major
########################################################
# Retourner les valeurs uniques de Major_category
all_ages_Major_category = all_ages["Major_category"].unique() # on rajoute unique()
# print(all_ages_Major_category)
# sans unique()
# 0      Agriculture & Natural Resources
# 1      Agriculture & Natural Resources
# ..... Name: Major_category, Length: 173, dtype: object
recent_grads_Major_category = recent_grads["Major_category"].unique()
# les ("Major_category") TypeError: 'DataFrame' object is not callable
# print(recent_grads_Major_category)

aa_cat_counts = {}
rg_cat_counts = {}

all_ages_Major_category_list = all_ages["Major_category"]
for major_cat in all_ages_Major_category:
    students_by_major = all_ages["Total"][all_ages_Major_category_list == major_cat]
    aa_cat_counts[major_cat]=students_by_major.sum()

# print(aa_cat_counts)


# Solution avec pivot table
aa_cat_counts_pt = all_ages.pivot_table(index="Major_category", values="Total", aggfunc=np.sum).to_dict('index')
# la clé est l'index de ligne
# value est un dictionnaire avec clé 'Total' et valeur la somme


recent_grads_Major_category_list = recent_grads["Major_category"]
for major_cat in recent_grads_Major_category:
    students_by_major = recent_grads["Total"][recent_grads_Major_category_list == major_cat]
    rg_cat_counts[major_cat]=students_by_major.sum()

# print(rg_cat_counts)


rg_cat_counts_pt = recent_grads.pivot_table(index="Major_category", values="Total", aggfunc=np.sum).to_dict('index')
# la clé est l'index de ligne
# value est un dictionnaire avec clé 'Total' et valeur la somme


def majorCatCounts(monDF):
    result={} # dico résultat
    monDFMClist = monDF["Major_category"]
    for majorC in monDFMClist:
        result[majorC] = monDF["Total"][monDFMClist==majorC].sum()
    return result
# print(majorCatCounts(recent_grads))
# print(majorCatCounts(all_ages))


########################################################
#######                    Taux de jobs à faible salaire
########################################################
serie_Total = recent_grads["Total"]
serie_Low_wage_jobs = recent_grads["Low_wage_jobs"]
low_wage_proportion =serie_Low_wage_jobs.sum() / serie_Total.sum()
print("Proportion de jeunes à faible salaire:", low_wage_proportion*100 ,'%.')


########################################################
#######                            Comparer des datasets
########################################################
rg_lower_count = 0
rg_lower_values_list = [] # () tuple et pas liste
rg_lower_major_list = []

# Séries des 2 DF sur l'étiquette "Major"
aa_major = all_ages["Major"]
rg_major = recent_grads["Major"]

for major in aa_major:
    # Sélection de l'employment rate pour la même major
    rows_unemployment_by_major_aa=all_ages["Unemployment_rate"][aa_major==major] # Serie
    rows_unemployment_by_major_rg=recent_grads["Unemployment_rate"][rg_major==major] # Serie
    # comparaison et compte
    if len(rows_unemployment_by_major_rg.values)>0 and len(rows_unemployment_by_major_aa.values)>0: # rajout cas PB crash sinon
        if rows_unemployment_by_major_rg.values[0] < rows_unemployment_by_major_aa.values[0]:
            rg_lower_count+=1
            rg_lower_values_list.append(float(rows_unemployment_by_major_rg.values[0]))
            rg_lower_major_list.append(major)

print("Total des nouveaux diplomés avec un meilleur tx 'umployment':",rg_lower_count)
# print(rg_lower_values_list)
# print(rg_lower_major_list)