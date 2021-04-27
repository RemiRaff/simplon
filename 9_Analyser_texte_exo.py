

# 1. Ecrire une fonction hascap(s) qui renvoie tous les mots de la chaîne
#     s commençant par une majuscule.
# Pour ce faire utiliser la fonction ord() pour obtenir le code ASCII des lettres
#     (Les lettres majuscule ont un code allant de 65 à 90).

def putcap(s):
    "Passe toutes les 1ere lettres en MAJ"
    maj,sreturn=True,""
    # for i in s:        print(i,ord(i)) # a = 97 A=65
    for i in range(len(s)):
        if maj: # cas où on doit mettre la 1ere minuscule en MAJ
            if ord(s[i])>=97: # sur une minuscule
                sreturn+=chr(ord(s[i])-32) # passe en MAJ
                maj=False
            elif ord(s[i])>=65 and ord(s[i])<=90: # sur une MAJ
                sreturn+=s[i]
                maj=False
            else: # autre chose
                sreturn+=s[i]
        else: # maj à false
            if ord(s[i])==32: # cas de ' ' pour début de mot
                maj=True
            sreturn+=s[i]
    return sreturn


def hascap(s):
    sreturn=[] # liste résultats
    ltravail=s.split() # liste de travail
    for i in ltravail:
        if 65<=ord(i[0]) and ord(i[0])<=90: # presence d'une MAJ rafik: if ord(m[0]) in range(65, 91):
            sreturn.append(i)
    return sreturn


# COR yanice
import re
def hascap_regex(s):
    m = re.findall(r'[A-Z]\w+', s)
    return m


mastr='Ma chaine  de caractères avec Beacoup de caractères Est bien faite.'
# mastr[32]='A' # ERREUR TypeError: 'str' object does not support item assignment
print(mastr)
print(putcap(mastr))
print(hascap(mastr))
print(hascap_regex(mastr))



# 2. Proposer une fonction inflation(s) qui va doubler la valeur de tout
#    les nombres dans la chaine s. Exemple : « Le prix est de 27 euros » devient « Le prix est de 54 euros ».
# Utiliser la fonction enumerate() pour lancer une boucle for (Taper dans Google « enumerate boucle for ».)

def inflation(s):
    sreturn=""
    stravail=s.split()
    for i in stravail:
        if i.isnumeric(): # i est un nombre en lettre
            monnb=float(i)
            sreturn+=str(monnb*2)+' '
        else:
            sreturn+=i+' '
    return sreturn


# COR rafik
def inflation_rafik(s):
    mots = s.split()
    for i, m in enumerate(mots):
        if m.isnumeric():
            mots[i]  = str(2*int(m))
    return " ".join(mots)

# COR yanice
# regex_euros='[-]?[0-9]+[\\.[0-9]*]?[euros|€|euro]?' # mon re
regex_euros = re.compile(r'([\d.]+) ?(?:€|euros)')
def inflate(phrase):
    matches = [s for s in re.findall(regex_euros, phrase)]
    matches.sort(reverse=True)
    for s in matches:
        phrase = phrase.replace(s, f'{float(s) * 2:.2f}')
    return phrase


s="Le prix est de 27 euros."
print(s)
print(inflation(s))
print(inflation_rafik("Le prix est de 27 euros"))
print(inflate(s))


# 3. Proposer une fonction lignes qui à partir d’une longue chaîne s (>100 caractères) renvoie une liste de chaîne
#    de caractères contenant chacun 24 caractères maximum et terminant par un espace.

def lignes(s):
    listemots=s.split()
    listereturn,ligne=[],""
    for i in listemots: # i est un mot
        if len(ligne)+len(i)+1 <= 24:
            ligne+=i+' '
        else:
            listereturn.append(ligne)
            ligne=i+' '
    # traitement du relicat
    listereturn.append(ligne)

    return listereturn


def lignes_rafik(s):
    mots = s.split()
    lignes  = ['']
    for m in mots:
        m += " "
        if len(lignes[-1])+len(m)<24:
            lignes[-1] += (m)
        else:
            lignes.append(m)
    return lignes

s = "Onze ans déjà que cela passe vite Vous "
s += "vous étiez servis simplement de vos armes la "
s += "mort n‘éblouit pas les yeux des partisans Vous "
s += "aviez vos portraits sur les murs de nos villes "
print(s)
print(lignes(s))
print(lignes_rafik(s))



# 4. Proposer un programme qui renvoie la liste de tout les nombres (y compris décimaux et négatifs) d’une chaîne de caractères.
#    A tester sur la chaîne : « Les 2 maquereaux valent 6.50 euros ».

from re import findall

def givenumbers(s):
    m='[-]?[0-9]+[\\.[0-9]*]?' # +{\.[0-9]*}?'           (\.[0-9]*)? faux il faut des []
    return findall(m,s)
# yohan return findall('-?\d+\S*',s)

s = "Les 2 maquereaux valent 6.50 euros avec une baisse de -2 euros."
print(s)
print(givenumbers(s))



# 5. Proposer une fonction arrondi(s) qui dans la chaîne s troncature tout les nombre décimaux. On autorise les nombres négatifs.
#    Pour ce faire, vous avez la possibilité d’utiliser :
#    - des () pour désigner des blocs de données dans l’expression rationnelle.
#    - pour remplacer chacun des blocs l’expression est r’\1_\2_’.

from re import sub

def arrondi(s):
    m='([-]?[0-9]+)([\\.[0-9]*]?)' # \\ pas nécessaire si entre [.]
    return sub(m,'\\1',s)


def tronc(s): # rafik
    motif = r"(-?)([0-9]+)[,.]?[0-9]*"
    return sub(motif, r"\1\2", s)

s="Les 2 maquereaux valent 6.50 euros avec une baisse de -2.20 euros."
print(s)
print(arrondi(s))
print(tronc(s))