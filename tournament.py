import random



def main(n,short): # https://fr.wikipedia.org/wiki/Table_de_Berger

    #init variables
    #global short  # raccourcir en enlevant les matchs doublons
    #short=s       #
    global cpt      # compteur de matchs
    cpt=0
    global matchlist# liste des matchs sous forme de tuples (ronde,joueur1,joueur2)
    matchlist=[]
    
    
    for r in range(1,n): #toutes les rondes de 1 à n-1
        for a in range(1,n+1): #tous joueurs a de 1 à n
            for b in range(1,n+1): #tous joueurs b de 1 à n
                #a=1
                #b=2
                if b!=n:
                    if a+b-1<n:
                        if r==a+b-1:
                            matchCreate(a,b,r,short)
                    else: # a+b-1>=n
                        if r==a+b-n:
                            matchCreate(a,b,r,short)
                else: # b=n
                    if 2*a<=n:
                        if r==2*a-1:
                            matchCreate(a,b,r,short)
                    else: # 2a>n
                        if r==2*a-n:
                            matchCreate(a,b,r,short)
    #print(cpt)
    return matchlist

def matchCreate(a,b,r,short):
    global cpt
    if a!=b: # enlever les matchs contre soi-même
        if short==True: # si short est True, on test le résultat de duplicateMatch
            if duplicateMatch(a,b)!=True:
                cpt=cpt+1
                matchlist.append((r,a,b))
                #print('Ronde {} : {} VS {}'.format(r,a,b))
        else:       #sinon on ignore duplicateMatch
                cpt=cpt+1
                matchlist.append((r,a,b))
                #print('Ronde {} : {} VS {}'.format(r,a,b))

def getMatchList():
    return matchlist

def duplicateMatch(p1,p2): #fonction vérifiant les matchs doublons, matchlist sert d'historique
    for i in matchlist:
        if i[2]==p1 and i[1]==p2:
            return True

if __name__ == '__main__':
    
    import sys
    sys.exit(main(6,True))