#from  tournoi_DB import getWins,getDraws,getLosses
#def main(n,short):
#    return getMatchList(n,short)

def getMatchList(n,short=True,Berger=False): # Fonction principale, retourne liste des matchs pour n joueurs
    global matchlist # Init liste des matchs sous forme de tuples (ronde,joueur1,joueur2), globale
    matchlist=[]
    if Berger==True: # choix méhode Berger ou ruban
        return methodeBerger(n,short)
    else:
        return methodeRuban(n,short)

def methodeBerger(n,short): # Méthode utilisant règles de la table de Berger
    #print('berger')
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

def methodeRuban(n,short): # Méthode du ruban, plus rapide
    #print('ruban')
    if n%2!=0:
        return [] # Sécurité: vérifier si nombre joueurs est bien pair
    Rb=[i for i in range(2,n+1)] # générer ruban de joueurs sauf le 1
    h=0
    b=int((n/2)-1) # initialiser les pointeurs

    for r in range(1,n):
        matchCreate(1,Rb[int(b+n/2-1)%(n-1)],r) # Cas du 1
        for i in range(0,int(n/2-2)+1):
            matchCreate(Rb[(h+i)%(n-1)],Rb[int(b+n/2-2-i)%(n-1)],r)
        h=(h-1)%(n-1)
        b=(b-1)%(n-1)
    return matchlist


def matchCreate(a,b,r,short=False): # Fonction ajoutant à matchlist un match entre a et b à la ronde r sous forme (r,a,b)
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

############### [TEMPORAIRE] Fonctions simulant les résultats récupérés par tournoi_DB. COMMENTER CECI et DECOMMENTER LA LIGNE 1 une fois les vraies fonctions terminées
def getWins(player):
    wins=[[2],[],[1,2,6],[1,2,3,5,6],[1,2,3],[1,2,5]]
    return wins[player-1]

def getDraws(player):
    draws=[[],[],[],[],[],[]]
    return draws[player-1]

def getLosses(player):
    losses=[[3,4,5,6],[1,3,4,5,6],[4,5],[],[4,6],[3,4]]
    return losses[player-1]
########################################################################################################################################################################
def useSecond(untuple): # Fonction retournant le 2e terme d'un tuple, utilisée comme clé pour sort()
    return untuple[1]

def classement(n,kw=1,kd=0,kl=0):
    classmt=[]
    for pl in range(1,n+1):
        classmt.append((pl,kw*len(getWins(pl))+kd*len(getDraws(pl))+kl*len(getLosses(pl))))
    classmt.sort(reverse=True,key=useSecond)
    return classmt


if __name__ == '__main__':
    import sys
    sys.exit(getMatchList(6,True,False))
    #sys.exit(classement(6))
