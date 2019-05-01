#! python3
# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, request
import sqlite3
import tournament
import tournoi_DB
app = Flask(__name__)   # Initialise l'application Flask




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

    #On récupère le choix sur la longueur du tournoi et on en fait un booléen
    Short=request.form['shortcheckbox']
    if Short == "0":
        Short=True
    elif Short=="1":
        Short=False

    #On récupère le choix sur les matchs de barrage et on en fait un booléen
    Barrages=request.form['match_barrages']
    if Barrages == "0":
        Barrages=True
    elif Barrages=="1":
        Barrages=False

    #On récupère la liste des matchs
    Matchlist=tournament.getMatchList(Nbr_player,Short)
    Nbr_matchs=len(Matchlist)

    #On crée les tables de la base de donnée
    tournoi_DB.openDB()
    tournoi_DB.createTables()
    #On donne la liste des joueurs à la base de donnée
    tournoi_DB.createPlayers(Players)

    #On crée une liste des matchs avec le pseudo des joueurs au lieu de leur IDs
    Matchlist_pseudo=tournament.getMatchList(Nbr_player,Short)
    for i in range(len(Matchlist_pseudo)):
        Matchlist_pseudo[i]=list(Matchlist_pseudo[i])
    for i in Matchlist_pseudo:
        i[1]=tournoi_DB.getPseudo(i[1])
        i[2]=tournoi_DB.getPseudo(i[2])
    print(Matchlist_pseudo)
    print(Matchlist)
    #On utilise le template display.html
    return render_template('display.html.j2' , players=Players ,nbr_player=Nbr_player, type_tournoi=Type_tournoi, matchlist=Matchlist, matchlist_pseudo=Matchlist_pseudo, nbr_matchs=Nbr_matchs)




@app.route('/results/', methods=['POST'])
def results():
    results=[]
    for i in range(1,Nbr_player+1) :
        #On récupère l'id des joueurs qui ont gagné pour les mattre dans la liste results
        results.append(request.form['match{}'.format(i)])

    #On utilise le template results.html
    return render_template('results.html.j2', nbr_player=Nbr_player, type_tournoi=Type_tournoi)




if __name__ == '__main__' :
    app.run(debug=True) #, host='192.168.1.91', port=int("443")
