
#def main(n,short): # https://fr.wikipedia.org/wiki/Table_de_Berger
#    return getMatchList(n,short)

def getMatchList(n,short=True,Berger=False):
    global matchlist # Init liste des matchs sous forme de tuples (ronde,joueur1,joueur2), globale
    matchlist=[]
    if Berger==True: # choix méhode Berger ou ruban
        return methodeBerger(n,short)
    else:
        return methodeRuban(n,short)

def methodeBerger(n,short):

    for r in range(1,n): #toutes les rondes de 1 à n-1
        for a in range(1,n+1): #tous joueurs a de 1 à n
            for b in range(1,n+1): #tous joueurs b de 1 à n
                if b!=n and a!=n:
                    if a+b-1<n:
                        if r==a+b-1:
                            matchCreate(a,b,r,short)
                            break
                    else: # a+b-1>=n
                        if r==a+b-n:
                            matchCreate(a,b,r,short)
                            break
                else:
                    if 2*a<=n:
                        if r==2*a-1:
                            matchCreate(a,b,r,short)
                            break
                    else: # 2a>n
                        if r==2*a-n:
                            matchCreate(a,b,r,short)
                            break
    return matchlist
def methodeRuban(n,short):
    if n%2!=0:
        return [] # Sécurité: vérifier si nombre joueurs est bien pair
    Rb=[i for i in range(2,n+1)] # générer ruban de joueurs sauf le 1
    h=0
    b=int((n/2)-1) # initialiser les pointeurs

    for r in range(1,n):
        matchCreate(1,Rb[int(b+n/2-1)%(n-1)],r,short) # Cas du 1
        for i in range(0,int(n/2-2)+1):
            matchCreate(Rb[(h+i)%(n-1)],Rb[int(b+n/2-2-i)%(n-1)],r,short)
        h=(h-1)%(n-1)
        b=(b-1)%(n-1)
    return matchlist


def matchCreate(a,b,r,short):
    if a!=b: # enlever les matchs contre soi-même
        if short==True: # si short est True, on test le résultat de duplicateMatch
            if duplicateMatch(a,b)!=True:
                matchlist.append((r,a,b))
                #print('Ronde {} : {} VS {}'.format(r,a,b))
        else:       #sinon on ignore duplicateMatch
                matchlist.append((r,a,b))
                #print('Ronde {} : {} VS {}'.format(r,a,b))


def duplicateMatch(p1,p2): #fonction vérifiant les matchs doublons, matchlist sert d'historique
    for i in matchlist:
        if i[2]==p1 and i[1]==p2:
            return True

if __name__ == '__main__':
    import sys
    sys.exit(getMatchList(14,False,True))
