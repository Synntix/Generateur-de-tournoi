import tournoi_DB

def getMatchList(n,extended=False,Berger=False,debug_algo=False): # Fonction principale, retourne liste des matchs pour n joueurs
    global debug
    debug=debug_algo # Astuce pour avoir une variable debug globale à partir d'un paramètre
    # Init liste matchs sous forme de tuples (ronde,joueur1,joueur2), *globale*
    global matchlist
    matchlist=[]
    global Bye
    if n%2==1:
        n+=1
        Bye=True
    else:
        Bye=False
    if debug:
        print("#ALGO# Nb joueurs = {} \n#ALGO# Bye = {}".format(n,Bye))
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
    if debug:
        print("#ALGO# Méthode Berger")
    if n%2!=0:
        return [] # Sécurité: vérifier si nombre joueurs est bien pair

    for r in range(1,n): #toutes les rondes de 1 à n-1
        for a in range(1,n+1): #tous joueurs a de 1 à n
            for b in range(1,n+1): #tous joueurs b de 1 à n
                if b!=n and a!=n:
                    if a+b-1<n:
                        if r==a+b-1:
                            matchCreate(n,a,b,r)
                            #break
                    else: # a+b-1>=n
                        if r==a+b-n:
                            matchCreate(n,a,b,r)
                            #break
                else:
                    if 2*a<=n:
                        if r==2*a-1:
                            matchCreate(n,a,b,r)
                            #break
                    else: # 2a>n
                        if r==2*a-n:
                            matchCreate(n,a,b,r)
                            #break
    return matchlist

def methodeRuban(n): # Méthode du ruban, plus rapide
    if debug:
        print("#ALGO# Méthode ruban")
    if n%2!=0:
        return [] # Sécurité: vérifier si nombre joueurs est bien pair
    Rb=[i for i in range(2,n+1)] # générer ruban de joueurs sauf le 1
    # initialiser les pointeurs
    h=0
    b=int((n/2)-1)

    for r in range(1,n):
        matchCreate(n,1,Rb[int(b+n/2-1)%(n-1)],r,False) # Cas du 1
        for i in range(0,int(n/2-2)+1): # Cas des autres matchs
            matchCreate(n,Rb[(h+i)%(n-1)],Rb[int(b+n/2-2-i)%(n-1)],r,False)
        # Décalage des pointeurs
        h=(h-1)%(n-1)
        b=(b-1)%(n-1)
    return matchlist

def matchCreate(n,a,b,r,verif=True): # Fonction ajoutant à matchlist un match entre a et b à la ronde r sous forme (r,a,b)
    if not verif: #possibilité d'éviter la vérification (pour ruban)
        if not Bye:
            matchlist.append((r,a,b))
        elif a!=n and b!=n:
            matchlist.append((r,a,b))

    elif a!=b and not duplicateMatch(a,b): # enlever les matchs contre soi-même et les doublons
        if not Bye:
            matchlist.append((r,a,b))
        elif a!=n and b!=n:
            matchlist.append((r,a,b))
            #print('Ronde {} : {} VS {}'.format(r,a,b))

def duplicateMatch(p1,p2): # Fonction vérifiant les matchs doublons, matchlist sert d'historique
    for i in matchlist:
        if i[2]==p1 and i[1]==p2:
            return True

def reverseMatchlist(n): # Fonction inversant les 2 joueurs de chaque tuple-match de matchlist, pour le tournoi étendu
    if debug:
        print("#ALGO# Ajout inversion matchlist")
    invlist=[(i[0]+n-1,i[2],i[1]) for i in matchlist]
    return invlist

def deuxiemeTerme(untuple): # Fonction retournant le 2e terme d'un tuple, utilisée comme clé pour sort()
    return untuple[1]

def getClassement(n,matchlist,win,kw=1,kd=0,kl=0,debug_algo=False): # Fonction de calcul des scores et du classement
    classement=[]
    nbMatchs=len(matchlist)
    if debug:
        print("#ALGO# Calcul score pour {} matchs".format(nbMatchs))
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
    if debug:
        print("#ALGO# Liste des victoires :\n",win)
        print("#ALGO# Liste des égalités :\n",draw)
        print("#ALGO# Liste des défaites \n",lose)
    for pl in range(1,n+1): #Calcul du score pour chaque joueur
        score=kw*win.count(pl)+kd*draw.count(pl)+kl*lose.count(pl)
        classement.append((pl,score))
        if debug:
            print("#ALGO# --Score joueur {} = {}".format(pl,score))
    if debug:
        print("#ALGO# Classement non ordonné :\n",classement)
    #Tri inversé en prenant le 2e terme (score)
    classement.sort(reverse=True,key=deuxiemeTerme)
    if debug:
        print("#ALGO# Classement :\n",classement)
    return classement

# Exécute getMatchList seulement si le programme est lancé seul (non importé)
if __name__ == '__main__':
    import sys
    sys.exit(getMatchList(5,False,False))
    #sys.exit(getClassement(6,getMatchList(6),[1,5,4,5,6,3,1,3,6,3,4,5,1,6,5]))
