import tournoi_DB

# Fonction principale, retourne liste des matchs pour n joueurs
def getMatchList(n,extended=False,Berger=False):
    # Init liste matchs sous forme de tuples (ronde,joueur1,joueur2), *globale*
    global matchlist
    matchlist=[]
    if Berger==True: # choix méhode Berger ou ruban
        if extended==True: # Ajout liste inversée si besoin
            return methodeBerger(n)+reverseMatchlist(n)
        else:
            return methodeBerger(n)
    else:
        if extended==True: # Ajout liste inversée si besoin
            return methodeRuban(n)+reverseMatchlist(n)
        else:
            return methodeRuban(n)


def methodeBerger(n): # Méthode utilisant règles de la table de Berger
    #print('berger')
    if n%2!=0:
        return [] # Sécurité: vérifier si nombre joueurs est bien pair

    for r in range(1,n): #toutes les rondes de 1 à n-1
        for a in range(1,n+1): #tous joueurs a de 1 à n
            for b in range(1,n+1): #tous joueurs b de 1 à n
                if b!=n and a!=n:
                    if a+b-1<n:
                        if r==a+b-1:
                            matchCreate(a,b,r)
                            #break
                    else: # a+b-1>=n
                        if r==a+b-n:
                            matchCreate(a,b,r)
                            #break
                else:
                    if 2*a<=n:
                        if r==2*a-1:
                            matchCreate(a,b,r)
                            #break
                    else: # 2a>n
                        if r==2*a-n:
                            matchCreate(a,b,r)
                            #break
    return matchlist

def methodeRuban(n): # Méthode du ruban, plus rapide
    #print('ruban')
    if n%2!=0:
        return [] # Sécurité: vérifier si nombre joueurs est bien pair
    Rb=[i for i in range(2,n+1)] # générer ruban de joueurs sauf le 1
    # initialiser les pointeurs
    h=0
    b=int((n/2)-1)

    for r in range(1,n):
        matchCreate(1,Rb[int(b+n/2-1)%(n-1)],r,False) # Cas du 1
        for i in range(0,int(n/2-2)+1): # Cas des autres matchs
            matchCreate(Rb[(h+i)%(n-1)],Rb[int(b+n/2-2-i)%(n-1)],r,False)
        # Décalage des pointeurs
        h=(h-1)%(n-1)
        b=(b-1)%(n-1)
    return matchlist

# Fonction ajoutant à matchlist un match entre a et b à la ronde r
# sous forme (r,a,b)
def matchCreate(a,b,r,verif=True):
    if not verif: #possibilité d'éviter la vérification (pour ruban)
        matchlist.append((r,a,b))
    elif a!=b and duplicateMatch(a,b)!=True:
    # enlever les matchs contre soi-même et les doublons
        matchlist.append((r,a,b))
        #print('Ronde {} : {} VS {}'.format(r,a,b))

#fonction vérifiant les matchs doublons, matchlist sert d'historique
def duplicateMatch(p1,p2):
    for i in matchlist:
        if i[2]==p1 and i[1]==p2:
            return True

# Fonction inversant les 2 joueurs de chaque tuple-match de matchlist,
# pour le tournoi étendu
def reverseMatchlist(n):
    invlist=[(i[0]+n-1,i[2],i[1]) for i in matchlist]
    return invlist

# Fonction retournant le 2e terme d'un tuple, utilisée comme clé pour sort()
def deuxiemeTerme(untuple):
    return untuple[1]

# Fonction de calcul des scores et du classement
def getClassement(n,matchlist,win,kw=1,kd=0,kl=0):
    classement=[]
    nbMatchs=len(matchlist)
    # win est la liste des gagnants (ex: win[4] donne le gagnant du 4e match)
    draw=[]
    lose=[]
    # On met l'id d'un joueur dans draw quand il fait une égalité
    # et dans lose quand il perd
    for i in range(0,nbMatchs):
        # Si le gagnant du match i est le joueur 1 du match i,
        if win[i]==matchlist[i][1]:
            # on ajoute le joueur 2 à lose
            lose.append(matchlist[i][2])
        elif win[i]==matchlist[i][2]: # sinon si le gagnant est le joueur 2,
            # on ajoute le joueur 1 à lose
            lose.append(matchlist[i][1])
        elif win[i]==0: # sinon si le gagnant est 0 (égalité)
            # on ajoute les deux joueurs à draw
            draw.append(matchlist[i][1])
            draw.append(matchlist[i][2])

    for pl in range(1,n+1): #Calcul du score pour chaque joueur
        classement.append((pl,kw*win.count(pl)+kd*draw.count(pl)+kl*lose.count(pl)))
    #Tri inversé en prenant le 2e terme (score)
    classement.sort(reverse=True,key=deuxiemeTerme)
    return classement

# Exécute getMatchList seulement si le programme est lancé seul (non importé)
if __name__ == '__main__':
    import sys
    sys.exit(getMatchList(6,False,True))
    #sys.exit(getClassement(6,getMatchList(6),[1,5,4,5,6,3,1,3,6,3,4,5,1,6,5]))
