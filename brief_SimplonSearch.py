#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 11 11:58:52 2021

@author: simplon
"""

# python_brief_SimplonSearch.pdf

import re

alpha=('a','z','e','r','t','y','u','i','o','p','q','s','d','f','g','h','j','k','l','m','w','x','c','v','b','n')

def variancemot(mot):
    result=[] # liste vide pour le résultat
    
    # toutes les poddibilités avec 1 lettre en moins
    for i in range(len(mot)):
        if i==0:
            result.append(mot[1:]) # mot.replace(i,'') pb ne gère pas les lettres en doublons
        else:
            result.append(mot[:i]+mot[i+1:])
    
    # toutes les possibilités avec 1 lettre en plus
    for i in range(len(mot)):
        for a in alpha:
            result.append(mot[:i]+a+mot[i:])
    for a in alpha:
        result.append(mot+a)
    
    # toutes les possibilités avec 1 lettre remplacée
    for i in range(len(mot)):
        for a in alpha:
            if i==0 and a!=mot[i]:
                result.append(a+mot[1:]) # mot.replace(i,'') pb ne gère pas les lettres en doublons
            elif a!=mot[i]:
                result.append(mot[:i]+a+mot[i+1:])
    
    return result
# print(variancemot("est"))


# recherche d'un mot dans une chaine
def almost(mot, s):
    # traitement de la phrase pour enlever la ponctuation et mettre ' ' entre chaque mot
    s = " "+re.sub("['.;,]",' ',s)+" "
    motif = "\s"+mot+"\s"

    found = re.findall(motif,s)

    for i in range(len(mot)):
        motif = "\s"+mot[:i]+mot[i+1:]+"\s"
        found += re.findall(motif,s) # .append(...) ajoute des [] en trop
    
    return found

s= "Les etrois tris, lys trois gros, les troisx roi."
mot = "trois"
print("almost:",almost(mot, s))


def almost_yanice(mot: str, s: str) -> list:
    words = ["".join([mot[j] if j != i else mot[j]+"?" for j in range(len(mot))]) for i in range(len(mot))]
    searchRegex = re.compile(r'[^a-z]('+ "|".join(words) +')[^a-z]', flags=re.IGNORECASE)
    return searchRegex.findall(" "+s)
print("almost Yanice:",almost_yanice(mot, s))


def pluslarge(mot, s):
    # traitement de la phrase pour enlever la ponctuation et mettre ' ' entre chaque mot
    s = " "+re.sub("['.;,]",' ',s)+" " # ajoute un ' ' eb début et fin pour traiter les mots en bordure
    motif = "\s"+mot+"\s"

    found = re.findall(motif,s) # recherche du mot exact

    # cas lettre manquante
    for i in range(len(mot)):
        motif = "\s"+mot[:i]+mot[i+1:]+"\s"
        found += re.findall(motif,s)

    # cas lettre en plus    
    for i in range(len(mot)):
        motif = "\s"+mot[:i]+"[^\s]{1}"+mot[i:]+"\s"
        found += re.findall(motif,s)
    # cas caractère en plus à la fin
    motif = "\s"+mot+"[^\s]{1}\s"
    found += re.findall(motif,s)

    # cas lettre remplacée    
    for i in range(len(mot)):
        motif = "\s"+mot[:i]+"[^\s^"+mot[i]+"]{1}"+mot[i+1:]+"\s" # {1} + gère aussi les lettres manquantes
        found += re.findall(motif,s)    
    return found


def CORpluslargeAntho(mot,s):
    z = " "+re.sub("[.,]","",s)+" "
    # Cas 1 : Une lettre en plus à la fin 
    motif_1 = "\s("+mot+")[^\s]\s"
    
    found = re.findall("\s("+mot+")\s",z)
    found += re.findall(motif_1, " "+z)


    for i in range(len(mot)):
        #motif = "\s"+mot[:i]+mot[i+1:]+"\s"
        
        # Cas 2 : Une lettre remplacée où lettre manquante
        motif_2 = "\s("+mot[:i]+"[^"+mot[i]+"]?"+mot[i+1:]+")\s"
        # Cas 3: Une lettre en plus
        motif_3 = "\s("+mot[:i]+"[^\s]"+mot[i:]+")\s"


        found += re.findall(motif_2, " "+z)
        found += re.findall(motif_3, " "+z)
    return found

def CORpluslargeYanice(mot, s):
    words = []
    for i in range(len(mot)):
        word = ""
        for j in range(len(mot)):
            word += mot[j] if j != i else mot[j]+"?.{0,1}"
        words.append(word)
    searchRegex = re.compile(r'\b('+ r"|".join(words) + r'|\w' + mot + r')\b', flags=re.IGNORECASE)
    return searchRegex.findall(s)

def CORpluslargeRafik(mot, s):
    z = " "+re.sub("[,.]", "", s)+ " "
    reg = []
    reg.append(mot+"[^\s]?")
    for i in range(len(mot)):
        # Je cherche le mot avec une lettre remplacé
        reg.append(mot[:i]+"[^"+mot[i]+"]?" + mot[i+1:])
        # Je cherche le mot avec une lettre en plus
        reg.append(mot[:i]+"[^\s]"+mot[i:])
    found = re.findall("\s("+"|".join(reg) + ")\s", " "+z)
    return found

s= "Les etrois tris, lys trois gros, les troisx roi troes."
mot = "trois"
print("pluslarge:",pluslarge(mot, s))
print("COR pluslarge Antho:",CORpluslargeAntho(mot, s))
print("COR pluslarge Yanice:",CORpluslargeYanice(mot, s))
print("COR pluslarge Rafik:",CORpluslargeRafik(mot, s))


def score(p,s):
    result=0
    p=re.sub("['.;,]",' ',p)
    s=re.sub("['.;,]",' ',s)
    pmots=p.split()
    smots=s.split()
    for pm in pmots:
        for sm in smots:
            if pm==sm:
                result+=5
                # print(pm,sm,result)
            else:
                for var in variancemot(sm):
                    if pm==var:
                        result+=1
                        # print(pm,sm,result)
    return result

ph1="C'est une phrase de test."
ph2="Le test est une chose utile pour la programmation."
print(ph1)
print(ph2)
print("Score:",score(ph1,ph2))


def score_v2(p,s):
    result=0
    p=re.sub("['.;,]",' ',p) # on nettoie les ponctuations, remplacées par ' '
    p=p.split() # tient compte que des ' '
    for i in p:
        found = pluslarge(i, s)
        for j in found:
            if i==j.strip().lower():
                result+=5
            else:
                result+=1
    return result
print(ph1)
print(ph2)
print("Score v2:",score_v2(ph1,ph2))

def CORscoreRafik(p, s):
    sc = 0
    q = " "+re.sub("[,.]","", p)+" "
    z = " " + re.sub("[,.]","", s)
    for x in q.split():
        sc += len(CORpluslargeRafik(x, s))
        sc += 4*z.count(" "+x+" ")
    return sc
print("Score Rafik:",CORscoreRafik(ph1,ph2))

def score_bonus(p,s):
    result,exactmatch=0,False
    p=re.sub("['.;,]",' ',p)
    p=p.split()
    for i in p:
        found = pluslarge(i, s)
        if found != []:
            if i==found[0].strip().lower(): # on enlève les blancs et on met en lower
                if exactmatch:
                    result+=20 # bonus
                else:
                    exactmatch=True
            else:
                exactmatch=False
        for j in found:
            if i==j.strip():
                result+=5
            else:
                result+=1
    return result
print(ph1)
print(ph2)
print("Score bonus:",score_bonus(ph1,ph2))
ph3 = "Le petit bonhomme en mousse"
ph4 = "Ce superbe matelas en mousse naturelle"
print(ph3+"\n"+ph4)
print("Score v2:",score_v2(ph3,ph4))
print("Score bonus:",score_bonus(ph3,ph4))

def CORscoreLuca(p, s):
    sc = 0
    q = " "+re.sub("[,.]","", p)+" "
    z = " " + re.sub("[,.]","", s)
    mot = p.split()
    for x in mot:
        for i in pluslarge(x, z):
            sc += 5 if i in q else 1
    for y in range(len(mot)-1):
        if " " + mot[y] + " " + mot[y+1] + " " in z:
            sc += 20
    return sc
print("Score Luca bonus:",CORscoreLuca(ph3,ph4))


############################################ Facultatif
import os

mon_path="/home/simplon/Téléchargements"
mes_fich=('Seaborn.txt', 'Matplotlib.txt', 'Pandas.txt', 'Numpy.txt')
ldir = os.listdir(mon_path)
# print(ldir)

fd_sea = open(mon_path+'/'+mes_fich[0], 'r', encoding="utf-8") # os.O_RDWR|os.O_CREAT
fd_mat = open(mon_path+'/'+mes_fich[1], 'r', encoding="utf-8") # pas avec os.open()
fd_pan = open(mon_path+'/'+mes_fich[2], 'r', encoding="utf-8")
fd_num = open(mon_path+'/'+mes_fich[3], 'r', encoding="utf-8")

sea_txt = fd_sea.read() # os.read() on doit mettre le nb de bytes
mat_txt = fd_mat.read()
pan_txt = fd_pan.read()
num_txt = fd_num.read()

fd_sea.close()
fd_mat.close()
fd_pan.close()
fd_num.close()

# print(sea_txt)
# print(mat_txt)
# print(pan_txt)
# print(num_txt)

mon_dico={}
s2search = "Analyse et visualisation"
mon_dico[mes_fich[0]] = score_bonus(s2search,sea_txt)
mon_dico[mes_fich[1]] = score_bonus(s2search,mat_txt)
mon_dico[mes_fich[2]] = score_bonus(s2search,pan_txt)
mon_dico[mes_fich[3]] = score_bonus(s2search,num_txt)
# print(mon_dico)

# Trie du dictionnaire
sorted_tuples = sorted(mon_dico.items(),key=lambda item: item[1],reverse=True)
# print(sorted_tuples)
sorted_dico = {k: v for k, v in sorted_tuples}
print("STR=", s2search)
print(sorted_dico)

# Yanice
# J'ai utilisé pour les regex, le paquet tiers "regex" et pas "re" de Python.
# Car le paquet "re" gère mal les caractères latin avec accents (c'est un
# paquet orienté anglo-saxon) et ne permet pas d'autoriser les overlap dans les match. 
# exemple:
# Avec re \b(.+)\b match pour le mot "téléphone" trois résultats: "t", "l", "phone"
# Avec regex \b(.+)\b match pour le mot "téléphone" un seul résultat: "téléphone"