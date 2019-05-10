#! python3
# -*- coding: utf-8 -*-
#title           :web_interface.py
#description     :Ce programme lance le serveur web du projet
#author          :Synntix
#date            :04/05/2019
#version         :0.1
#python_version  :3.7
#=======================================================================
from flask import Flask, render_template, url_for, request
import sqlite3
import tournament
import tournoi_DB
app = Flask(__name__)   # Initialise l'application Flask
debug=True



@app.route('/')  #C'est un décorateur, on donne la route ici "/"  l'adresse sera donc localhost:5000/
def accueil():
    #On utilise le template accueil.html, avec les variables titre et lignes
    return render_template("accueil.html.j2")




@app.route('/player_entry/', methods=['POST'])
def player_entry():
    global Nbr_player
    global Type_tournoi
    global Pts_win
    global Pts_draw
    global Pts_lose
    Nbr_player=int(request.form['nbr_player'])
    Type_tournoi=request.form['type_tournoi']
    Pts_win=int(request.form['pts_win'])
    Pts_draw=int(request.form['pts_draw'])
    Pts_lose=int(request.form['pts_lose'])

    if debug==True:
        print("Nombre de joueurs : {}".format(Nbr_player))
        print("Type de tournoi : {}".format(Type_tournoi))
        print("Nombre de points par match gagné : {}".format(Pts_win))
        print("Nombre de points par égalité : {}".format(Pts_draw))
        print("Nombre de points par match perdu : {}".format(Pts_lose))

    #On utilise le template page2.html
    return render_template('page2.html.j2' , nbr_player=Nbr_player, type_tournoi=Type_tournoi)




@app.route('/display/', methods=['POST'])
def display():
    #On crée la liste 'Players' et on ajoute tous les pseudo des participants
    global Players
    Players=[]
    for i in range(1,Nbr_player+1) :
        #On ajoute le pseudo des joueurs à la liste "Players"
        Players.append(request.form['pseudo{}'.format(i)])
    if debug==True:
        print("Liste des joueurs :\n{}".format(Players))

    #On récupère le choix sur la longueur du tournoi et on en fait un booléen
    Extended=request.form['shortcheckbox']
    if Extended == "0":
        Extended=True
    elif Extended=="1":
        Extended=False
    if debug==True:
        print("Extended = {}".format(Extended))

    #On récupère le choix sur les matchs de barrage et on en fait un booléen
    Barrages=request.form['match_barrages']
    if Barrages == "0":
        Barrages=True
    elif Barrages=="1":
        Barrages=False
    if debug==True:
        print("Barrages = {}".format(Barrages))

    #On récupère la liste des matchs
    global Matchlist
    Matchlist=tournament.getMatchList(Nbr_player,Extended)
    if debug==True:
        print("Liste des matchs par ID :\n{}".format(Matchlist))
    global Nbr_matchs
    Nbr_matchs=len(Matchlist)

    #On crée les tables de la base de donnée
    tournoi_DB.openDB()
    tournoi_DB.createTables()
    #On donne la liste des joueurs à la base de donnée
    tournoi_DB.createPlayers(Players)

    #On crée une liste des matchs avec le pseudo des joueurs au lieu de leur IDs
    Matchlist_pseudo=tournament.getMatchList(Nbr_player,Extended)
    for i in range(len(Matchlist_pseudo)):
        Matchlist_pseudo[i]=list(Matchlist_pseudo[i])
    for i in Matchlist_pseudo:
        i[1]=tournoi_DB.getPseudo(i[1])
        i[2]=tournoi_DB.getPseudo(i[2])
    if debug==True:
        print("Liste des matchs par pseudo : \n{}".format(Matchlist_pseudo))

    #On utilise le template display.html
    return render_template('display.html.j2' , players=Players ,nbr_player=Nbr_player, type_tournoi=Type_tournoi, matchlist=Matchlist, matchlist_pseudo=Matchlist_pseudo, nbr_matchs=Nbr_matchs)




@app.route('/results/', methods=['POST'])
def results():
    results=[]
    for i in range(1,Nbr_matchs+1) :
        #On récupère l'id des joueurs qui ont gagné pour les mettre dans la liste results
        results.append(int(request.form['match{}'.format(i)]))
    if debug==True:
        print("Liste des IDs des gagnants (0 = égalité) : \n{}".format(results))

        win=[]
        draw=[]
        lose=[]
    #On met l'id d'un joueur dans win quand il gagne, dans draw quand il fait une égalité et dans lose quand il perd
    for i in range(Nbr_matchs):
        if results[i]==Matchlist[i][1]:
            win.append(Matchlist[i][1])
            lose.append(Matchlist[i][2])
        elif results[i]==Matchlist[i][2]:
            win.append(Matchlist[i][2])
            lose.append(Matchlist[i][1])
        elif results[i]==0:
            draw.append(Matchlist[i][1])
            draw.append(Matchlist[i][2])
    if debug==True:
        print("win : {}".format(win))
        print("draw : {}".format(draw))
        print("lose : {}".format(lose))

    #On compte les points de chaque joueurs. Les points sont associés au joueur avec un dictionnaire
    Points = {}
    for i in range(1,len(Players)+1):
        Points[i]=win.count(i)*Pts_win
        Points[i]+=draw.count(i)*Pts_draw
        Points[i]+=lose.count(i)*Pts_lose
    if debug==True:
        print(Points)

    #On calcule le nombre de points maximum et minimum
    Pts_max=Matchlist[-1][0]*Pts_win
    Pts_min=Matchlist[-1][0]*Pts_lose

    #On trie par ordre décroissant les joueurs en fonction de leur nombre de points dans Classement
    Classement=[]
    for i in range (Pts_max,Pts_min,-1):
        for id in range (1,len(Players)+1):
            if Points[id]==i:
                Classement.append(id)
    if debug==True:
        print(Classement)

    Classement_pseudo=[]
    for i in range(len(Classement)):
        Classement_pseudo.append(tournoi_DB.getPseudo(Classement[i]))

    #On utilise le template results.html
    return render_template('results.html.j2', nbr_player=Nbr_player, type_tournoi=Type_tournoi, points=Points, classement_pseudo=Classement_pseudo, classement=Classement)




if __name__ == '__main__' :
    app.run(debug=True, port=int("80"))
