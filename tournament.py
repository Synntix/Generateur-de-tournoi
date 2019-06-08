
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
        print("#A# Nb joueurs = {} \n#A# Bye = {}\n#A# Extended = {}".format(n,Bye,extended))
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
        print("#A# Méthode Berger")
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
        print("#A# Méthode ruban")
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
        print("#A# Ajout inversion matchlist")
    invlist=[(i[0]+n-1,i[2],i[1]) for i in matchlist]
    return invlist

def terme2(untuple): # Fonction retournant le 2e terme d'un tuple, utilisée comme clé pour sort()
    return untuple[1]
def terme3(liste): # Fonction retournant le 2e terme d'un tuple, utilisée comme clé pour sort()
    return liste[2]
def getClassement(n,matchlist,results,scoremode=False,kw=1,kd=0,kl=0,debug=False): # Fonction de calcul des scores et du classement
    from copy import deepcopy
    classement=[]
    scores=[[i,0] for i in range(1,n+1)]
    nbMatchs=len(matchlist)
    if debug:
        print("#A# Liste des matchs :\n",matchlist)
        if scoremode:
            print("#A# Mode : Scores")
            #for i in range (nbMatchs):

        else:
            print("#A# Mode : Tout Ou Rien")
            #for i in range (nbMatchs):
                #print("Ronde {} - Match {}\n                    {} VS {}\n         Résultat : {} gagne".format(matchlist[i][0],i+1,matchlist[i][1],matchlist[i][2],results[i]))
        print("#A# Résultats :\n",results)

        print("#A# Calcul score pour {} matchs".format(nbMatchs))
    win=[[] for i in range(n)]
    draw=deepcopy(win)
    lose=deepcopy(win)

    if scoremode:
        for i in range(nbMatchs):
            scorej1=results[i][0]
            scorej2=results[i][1]
            scores[matchlist[i][1]-1][1]+=scorej1
            scores[matchlist[i][2]-1][1]+=scorej2
            if scorej1>scorej2:
                winner=matchlist[i][1]
                loser=matchlist[i][2]
                if debug:
                    print("Ronde {} - Match n°{}\n           Joueurs :   {} VS {}\n            Points :   {} || {}\n     Issue (bonus) : V({})||D({})\n".format(matchlist[i][0],i+1,matchlist[i][1],matchlist[i][2],results[i][0],results[i][1],kw,kl))
            elif scorej1<scorej2:
                winner=matchlist[i][2]
                loser=matchlist[i][1]
                if debug:
                    print("Ronde {} - Match n°{}\n           Joueurs :   {} VS {}\n            Points :   {} || {}\n     Issue (bonus) : D({})||V({})\n".format(matchlist[i][0],i+1,matchlist[i][1],matchlist[i][2],results[i][0],results[i][1],kl,kw))
            else:
                draw[matchlist[i][1]-1].append(matchlist[i][2]) # pas de perdant, les deux vont dans la liste d'égalités de l'autre
                draw[matchlist[i][2]-1].append(matchlist[i][1])
                if debug:
                    print("Ronde {} - Match n°{}\n           Joueurs :   {} VS {}\n            Points :   {} || {}\n     Issue (bonus) : E({})||E({})\n".format(matchlist[i][0],i+1,matchlist[i][1],matchlist[i][2],results[i][0],results[i][1],kd,kd))
                continue

            win[winner-1].append(loser)
            lose[loser-1].append(winner)

        if debug:
            print("#A# Scores : ",scores)
    else:
        for i in range(nbMatchs):
            # On a accès au gagnant avec results[i], donc on définit loser pour avoir accès au perdant
            if results[i] == matchlist[i][1]: # Si le gagnant du match i est le joueur 1 du match i,
                loser=matchlist[i][2] # le perdant est le joueur 2
            elif results[i] == matchlist[i][2]: # sinon si le gagnant est le joueur 2,
                loser=matchlist[i][1] # le perdant est le joueur 1
            elif results[i] == 0: # sinon si le gagnant est 0 (égalité)
                draw[matchlist[i][1]-1].append(matchlist[i][2]) # pas de perdant, les deux vont dans la liste d'égalités de l'autre
                draw[matchlist[i][2]-1].append(matchlist[i][1])
                if debug:
                    print("Ronde {} - Match n°{} : {}\n                         Résultat : {} donc égalité".format(matchlist[i][0],i,matchlist[i],results[i]))
                continue
        # Ici le gagnant est results[i], le perdant est loser
            win[results[i]-1].append(loser) # On ajoute le perdant à la liste de victoires du gagnant
            lose[loser-1].append(results[i]) # On ajoute le gagnant à la liste de défaites du perdant
            if debug:
                print("Ronde {} - Match n°{} : {}\n                         Résultat : {} gagne donc {} perd".format(matchlist[i][0],i,matchlist[i],results[i],loser))

    if debug:
        print("#A# Liste des victoires :\n",win)
        print("#A# Liste des égalités :\n",draw)
        print("#A# Liste des défaites \n",lose)


    for pl in range(1,n+1): #Calcul du score pour chaque joueur
        score = kw*len(win[pl-1]) + kd*len(draw[pl-1]) + kl*len(lose[pl-1])
        scores[pl-1][1]+=score
    for i in scores: # Une fois les scores obtenus, calcul du score Sonneborn-Berger pour chaque joueur
        i.append(getSonnBerg(i[0],scores,win,draw))
        if debug:
            print("#A# -- Joueur : {} | Score : {} | SonnBerg : {}".format(i[0],i[1],i[2]))
    if debug:
        print("#A# Classement non ordonné :\n",scores)

    classement=bubbleSort(scores,win) # Tri à bulles suivant les 3 critères
    classement.reverse() # On inverse pour avoir un classement décroissant
    if debug:
        print("#A# Classement ordonné :\n",classement)
    return classement

def getSonnBerg(pl,scores,win,draw): # Fonction de calcul du score Sonneborn-Berger (SBscore)) pour le joueur pl
    SBscore=0 # Init SBscore à 0
    for adv in win[pl-1]:           # Pour chaque adversaire contre qui pl a gagné,
         SBscore += scores[adv-1][1]   # on ajoute son score au SBscore
    for adv in draw[pl-1]:          # Et pour chaque adversaire contre qui pl a égalisé,
         SBscore += scores[adv-1][1]/2 # on ajoute la moitié de son score au SBscore
    return SBscore

def bubbleSort(scores,win): # Fonction de tri "à bulles" de scores, le meilleur joueur à la fin
    n = len(scores)
    for i in range(n): # Pour tous les éléments de la liste
        for j in range(0, n-i-1): # On traverse de 0 à n-i-1
            # et si le joueur j est meilleur (voir conditions) que le joueur j+1, on passe j devant j+1 (inversion)
            # Conditions :
            if scores[j][1] > scores[j+1][1] :      # Score de j meilleur
                scores[j], scores[j+1] = scores[j+1], scores[j]
            elif scores[j][1] == scores[j+1][1]:
                if scores[j][2] > scores[j+1][2]:   # ou Scores égaux ET score SonnBerg de j meilleur
                    scores[j], scores[j+1] = scores[j+1], scores[j]
                elif scores[j][2] == scores[j+1][2] and scores[j+1][0] in win[scores[j][0]-1]:
                    # ou Scores égaux, scores SonnBerg égaux et j a gagné contre j+1 (càd j+1 est dans la liste de victoires de j)
                    scores[j], scores[j+1] = scores[j+1], scores[j]
    return scores


def SimulateRandom(nbjoueurs,extended=False,berger=False,scoremode=False,kwin=1,kdraw=0,klose=0):
    from random import choice,randrange
    from time import time
    start_time=time()
    prev_time=time()
    test_matchlist=getMatchList(nbjoueurs,extended,berger,True)
    print('        getMatchList execution time : {} ms'.format((time()-prev_time)*1000))

    if scoremode:
        test_results=[(randrange(0,4),randrange(0,4)) for i in test_matchlist]
    else:
        test_results=[choice([i[1],i[2],0]) for i in test_matchlist]

    prev_time=time()
    getClassement(nbjoueurs,test_matchlist,test_results,scoremode,kwin,kdraw,klose,True)
    print('        getClassement execution time : {} ms'.format((time()-prev_time)*1000))

# Exécute getMatchList seulement si le programme est lancé seul (non importé)
if __name__ == '__main__':
    import sys
    #sys.exit(getMatchList(6,False,False))
    #sys.exit(getClassement(6,[(1, 1, 6), (1, 2, 5), (1, 3, 4), (2, 1, 5), (2, 6, 4), (2, 2, 3), (3, 1, 4), (3, 5, 3), (3, 6, 2), (4, 1, 3), (4, 4, 2), (4, 5, 6), (5, 1, 2), (5, 3, 6), (5, 4, 5)],[1,5,4,5,6,3,1,3,6,3,4,5,1,6,5],1,0,0,True))
    sys.exit(SimulateRandom(6))
