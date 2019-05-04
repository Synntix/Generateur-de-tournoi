#! python3
# -*- coding: utf-8 -*-
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
        results.append(request.form['match{}'.format(i)])
    if debug==True:
        print("Liste des IDs des gagnants (0 = égalité) : \n{}".format(results))

    #On utilise le template results.html
    return render_template('results.html.j2', nbr_player=Nbr_player, type_tournoi=Type_tournoi)




if __name__ == '__main__' :
    app.run(debug=True) #, host='192.168.1.91', port=int("443")
