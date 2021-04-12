import random

#choix du mot à deviner, par le logiciel , avant tout essai de l'utilisateur

mots=["CHEVAL","POUSSIN","POULE","COQ","GRENOUILLE","ASTICOT","VER","ALUMINIUM","CARTON","BOUC","CERISIER","POMMIER","KIMONO","BATTE"]

motATrouve=mots[random.randint(0,len(mots)-1)]

print("Jeux du pendu!")

char1=input("Donnez vos lettres et valisez avec entrée: ")
char1=char1.upper()
for i in motATrouve:
    if char1 == i:
        print(char1+' ',end='') # ,sep=' '
    else:
        print("# ",end='')

char2=input("\n")
char2=char2.upper()
for i in motATrouve:
    if char2 == i:
        print(char2+' ',end='') # ,sep=' '
    else:
        print("# ",end='')
        
char3=input()
char3=char3.upper()
for i in motATrouve:
    if char3 == i:
        print(char3+' ',end='') # ,sep=' '
    else:
        print("# ",end='')
        
char4=input()
char4=char4.upper()
for i in motATrouve:
    if char4 == i:
        print(char4+' ',end='') # ,sep=' '
    else:
        print("# ",end='')
        
char5=input()
char5=char5.upper()
for i in motATrouve:
    if char5 == i:
        print(char5+' ',end='') # ,sep=' '
    else:
        print("# ",end='')

char6=input()
char6=char6.upper()
for i in motATrouve:
    if char6 == i:
        print(char6+' ',end='') # ,sep=' '
    else:
        print("# ",end='')

proposition=(input("Donnez votre proposition: ")).upper()
if proposition==motATrouve:
    print("GAGNE")
else:
    print("PERDU, le mot était: ",motATrouve)
