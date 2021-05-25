#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 19 14:47:11 2021

@author: Marigleta, Yoan, Brahiman et Rémi
"""

import random


class Case:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self,other):
        "Surchage de == pour comparer 2 cases en valeurs"
        # http://lptms.u-psud.fr/wiki-cours/index.php/Python:_Surcharge
        return (self.x == other.x) and (self.y == other.y)
    def __str__(self):
        "Affichage pour str()"
        return "Case: x="+str(self.x)+" , y="+str(self.y)
    def __repr__(self):
        "Affichage pour repr()"
        return "("+str(self.x)+", "+str(self.y)+")"
    def casesAdjacentes(self,jeu):
        "Retourne une liste contenant les cases adjacentes possibles"
        l=[]
        # jeu est passé en paramètre pour récupérer le damier: liste de Cases
        for i in range(-1,2):
            for j in range(-1,2):
                c=Case(self.x+i,self.y+j)
                if jeu.surDamier(c):
                    l.append(c)
        l.remove(self) # sinon nous pouvons rester à même place
        return l


class Créature:
    def __init__(self,nom,c):
        self.nom = nom
        self.position = c # c est une Case
    def __str__(self):
        return self.nom+" est sur "+str(self.position)
    def __repr__(self):
        return self.nom+" est sur "+str(self.position)
    def choisirCible(self,jeu):
        lPosAdj = self.position.casesAdjacentes(jeu)
        for i in lPosAdj:
            if jeu.estOccupée(i): # caseAdjacente i est occupée, on la choisit
                return i
        return lPosAdj[random.randint(0,len(lPosAdj)-1)]
    def initiale(self):
        return self.nom[0]


class Jeu:
    def __init__(self, listeDesCréatures, dimension):
        "Arguments: liste de créatures, dimension du damier (x,y)"
        self.x = dimension[0]
        self.y = dimension[1]
        # liste de liste de Case permet la création d'un damier
        # sans utiliser c.__eq__()
        # obligation de placer les cr sur le damier
        self.listeDesCréatures = listeDesCréatures
        self.tour = 0
        self.actif = True # correction actif = cr pour la créature active

    def __str__(self):
        s = ""
        for i in self.listeDesCréatures:
            print(i)
        s = "Tour: "+str(self.tour)+" actif: "+str(self.actif)
        return s
    def estOccupée(self,c):
        for i in self.listeDesCréatures:
            if i.position == c:
                return True
        return False
    def surDamier(self,c):
        return (0 <= c.x and c.x<=self.x) and (0 <= c.y and c.y<=self.y)
    def deplacer(self,cr,c):
        if self.estOccupée(c):
            for i in self.listeDesCréatures:
                if i.position == c:
                    self.listeDesCréatures.remove(i)
                    if len(self.listeDesCréatures) == 1:
                        self.actif=False
        cr.position = c
        print(cr)
    def afficherPositions(self):
        for i in range(self.y+1):
            line=""
            for j in range(self.x+1):
                c,vide=Case(j,i),True
                for cr in self.listeDesCréatures:
                    if cr.position == c:
                        line+=cr.initiale()+' '
                        vide=False
                if vide:
                    line+=". "
            print(line)


# initialisation
damier = (4,5) # nb de cases pour le coté du damier 0-x et 0-y
cr1 = Créature("Lucifer",Case(0,0)) # positionner sur la case 1,1
cr2 = Créature("Michel",Case(damier[0],damier[1])) # positionner à l'opposé
cr3 = Créature("Adam", Case(damier[0]//2,damier[1]//2))
l =[cr1,cr2,cr3]
j = Jeu(l,damier) # création de l'objet j de type Jeu


j.afficherPositions()
while j.actif:
    for i in j.listeDesCréatures:
        j.deplacer(i,i.choisirCible(j))
        j.afficherPositions()
    j.tour+=1

print(j.listeDesCréatures[0].nom+" a gagné en "+str(j.tour)+" tours.")

# UML
# https://medium.com/@ganesh.alalasundaram/uml-diagram-using-pyreverse-for-python-repository-dd68cdf9e7e1
