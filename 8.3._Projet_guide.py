#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 14:48:21 2021

@author: simplon
"""

################# Projet guidé: Analyse de data
# support: 8.3._Projet_guide.pdf
# donnée: thanksgiving.csv


##############################################################################
# Introduction au dataset
##############################################################################
import pandas as pd

data = pd.read_csv('/home/simplon/thanksgiving.csv', encoding='latin-1')

# print(data.head())
# R: [5 rows x 65 columns]

data_columns = data.columns
# print(data_columns)
# columns = question


##############################################################################
# Filtrer des données
##############################################################################
data_celebrate = data['Do you celebrate Thanksgiving?']
data_celebrate_unique = data['Do you celebrate Thanksgiving?'].unique()
# print(data_celebrate) # serie de Yes No

# print(data_celebrate_unique)
# ['Yes' 'No']

# print(data_celebrate.value_counts())
# R: Yes    980       No      78
data_celebrate_yes = data_celebrate == 'Yes' # masque pour filtre
data = data[:][data_celebrate_yes]

# print(data.head())
# [5 rows x 65 columns]


##############################################################################
# Exploration des repas de thanksgiving
##############################################################################
col_name = 'What is typically the main dish at your Thanksgiving dinner?'
# print(data[col_name])
# Name: What is typically the main dish at your Thanksgiving dinner?, Length: 980, dtype: object
# print(data[col_name].value_counts()) # value_count() fait un Total par réponse
# Turkey                    859 .... Turducken                   3

col_name_gravy = 'Do you typically have gravy?'
tofurkey = data[col_name] == 'Tofurkey'
# print(data[col_name_gravy][tofurkey])
# 4      Yes ..... 953    Yes


##############################################################################
# Tendances des desserts pour Thanksgiving
##############################################################################
col_name='Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Apple'
data_pie = data[col_name]
apple_isnull = pd.isnull(data_pie) # serie de boolean

col_name='Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Pumpkin'
pumpkin_isnull = pd.isnull(data[col_name])

col_name='Which type of pie is typically served at your Thanksgiving dinner? Please select all that apply. - Pecan'
pecan_isnull = pd.isnull(data[col_name])

pies = apple_isnull & pumpkin_isnull & pecan_isnull

# print(pies.unique()) # [False  True]
# print(pies.value_counts())
# False    876
# True     104
# dtype: int64


##############################################################################
# 8.3._Projet_guide_-_Thanksgiving_-_complet.pdf
# Part 2
##############################################################################
import re
def agestr2int(mach):
    if pd.isnull(mach): # cas nan
        return None
    else: # cas "30 - 44" ou "60+"
        return int(re.findall('[0-9]+',mach)[0]) # match retourne un objet re
        

data["int_age"] = data['Age'].apply(agestr2int)
print(data["int_age"].describe())




def revenu2int(string):
    if pd.isnull(string):
        return None
    s=string.split()[0]
    if s=='Prefer':
        return None
    else:
        s=s.replace('$','')
        s=s.replace(',','')
        return int(s)

quest='How much total combined money did all members of your HOUSEHOLD earn last year?'
data['int_income'] = data[quest].apply(revenu2int)
print(data['int_income'].describe())



# < 150000 $
filtre_pauvre = data["int_income"] < 150000
quest='How far will you travel for Thanksgiving?'
result=data[quest][filtre_pauvre].value_counts()
print(result)

filtre_riche = data["int_income"] >= 150000
result=data[quest][filtre_riche].value_counts()
print(result)


# pivot_table
q1='Have you ever tried to meet up with hometown friends on Thanksgiving night?'
q2='Have you ever attended a "Friendsgiving?"'
print(pd.pivot_table(data,values='int_age',index=q1,columns=q2))

print(pd.pivot_table(data,values='int_income',index=q1,columns=q2))