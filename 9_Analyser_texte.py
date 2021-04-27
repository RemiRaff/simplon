a = 2

def test():
    global a # avec global on a 3 et 3 sans 2,3
    a = 3 # sans global et sans a= 3 on a 2,2
    print("Dans test:", a)


test()
# print("Après test:",a)

###############################################################################

def recursive_test(x):
    if x/2<1:
        print("Je ne m'appelle plus pour x=",x)
        return 1
    else:
        print("Je m'appelle pour x=",x)
        return recursive_test(x/2)+1

recursive_test(10)


def show_letter(letters):
    if (len(letters) > 0):
        print(letters.pop())
        show_letter(letters)


show_letter(list("! tulaS"))

#########################################################################

s1 ="Du passé faisons table rase."
l1 =[i for i in s1]
l2 = s1.split("as")
l3=s1.split()

print(l1[0],l1[1],l1[2],l1[3])
print(l2)
print(l3)

##################################################################################################

l1 = ['H','e','l','l','o',' ','W']
l2 = ['Du', 'passé', 'faisons', 'table', 'rase.']
s1 = "".join(l1)
s2 = " ".join(l2) # ' ' mis entre les elem de la liste

print(s1)
print(s2)

####################################################################################################

s1 = "Faisons table rase"
s2 = s1[:8].lower() + s1[8:13].upper()
print(s2)

#####################################################################################################

# chaine de caractères avec des prénoms séparés par des virgules
mon_csv = "Anthony Marais,Alex Beuil,Brahiman,Julien Bosse"
# on peut transformer la chaine en list de prénoms en splittant au niveau des virgules
print(mon_csv.split(',')) # résultat: ['Anthony Marais', 'Alex Beuil', 'Brahiman', 'Julien Bosse']

#####################################################################################

s1 = "Ce texte contient deux fois le mot texte."
print(s1.find('texte',0)) # R: 3
print(s1.find('texte',4)) # R: 35
print(s1.find('texte',36)) # R: -1

mon_max= 0
while mon_max>-1:
    mon_max=s1.find('texte',mon_max+1)
    print(mon_max)

################################################################################

s1 = "Le prix est de deux euros."
if 'euros' in s1:
    i=s1.index('euros')
    # print(i) # R: 20
    s2=s1[:i-5]+'$'+s1[i-5:i] # slicing ajout du $ devant deux et enlève euros.
    # print(s1[:i-5]) # R: Le prix est de
    # print(s1[i-5:i]) # R: deux
    j=s2.find('deux')
    s3=s2[:j]+'2.15'+s2[j+4:]
    print(s3)

##########################################""

s1 = 'Le prix est de deux euros.'
s2 = s1.replace('deux euros','$2.15')
print(s2)

############################################""

s='300 seulement ?'
l = s.split()
for mot in l:
    if mot.isalpha():
        print("mot")
    elif mot.isnumeric():
        print('nombre')
    if not mot.isalnum():
        print('?')

###############################################################################################

from re import findall
s= "Le PIB de l'Argentine baisse depuis 3 ans."
l1 = findall('[A-Z][a-z]+',s) # mot commençant par Majucule puis minuscule
l2 = findall('[a-zA-Z]*[iI][a-zA-Z]*',s) # mot avec un i ou I [A-z] peut fonctionner AVOIR
print(l1)
print(l2)
# R : ['Le', 'Argentine']
# R : ['PIB', 'Argentine', 'baisse', 'depuis']
# . N'importe quoi
# [xy] x ou y
# [x-y] entre x et y
# [^x] tout sauf x
# \s ' ' ou tab
# ^début de ligne
# $ fin de ligne
# xy x puis y
# {x}
# (?:abc){1-3} abc présent 1 à 3 fois succéssif
# ? correspond à {,1}
# + correspond à {1,}
# * correspond à {0,}

motif='0[1-9](?:[\\s\\.]?[0-9]{2}){4}'
n1="0678828383"
n2="09.34.67.12.11"
n3="03 11 23 20 38"
n4="03 11 23 20,"
n5="03.11 23 2038"
n6="03-23-20-20-38"
s=n1+n2+n3+n4+n5+n6
print(findall(motif,s)) # rend une liste de chaine valide


###################################################################################"""
# balise dans texte
from re import sub
s = 'Un texte <strong>HTML<strong/>avec des balises'
s += ' et même<script type="text/javascript">'
s += 'var i = 5 ;</script> du javascript dedans.'
s1= sub('<[a-z]*>','',s) # cherche motif puis le remplace
print(s1)
s2= sub('<.*>','',s)
s3= sub('<[a-z\\/"=\\s]*>','',s)
s4= sub('<[^>]*>','',s)
print(s2)
print(s3)
print(s4)