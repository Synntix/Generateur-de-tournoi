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
    Short=request.form['shortcheckbox']
    if Short == "0":
        Short=False
    elif Short=="1":
        Short=True

    tournament.main(Nbr_player,Short)
    return render_template('page2.html.j2' , nbr_player=Nbr_player, type_tournoi=Type_tournoi)

@app.route('/display/', methods=['POST'])
def display():
    #On crée la liste 'Players' et on ajoute tous les pseudo des participants
    global Players
    Players=[]
    for i in range(1,Nbr_player+1) :
        Players.append(request.form['pseudo{}'.format(i)])
    Matchlist=tournament.getMatchList()
    Nbr_matchs=len(Matchlist)
    #On crée les tables de la base de donnée
    #tournoi_DB.main()
    #On donne la liste des joueurs à la base de donnée
    #tournoi_DB.getid(Players)
    #On utilise le template accueil.html, avec les variables titre et lignes
    return render_template('display.html.j2' , players=Players ,nbr_player=Nbr_player, type_tournoi=Type_tournoi, matchlist=Matchlist, nbr_matchs=Nbr_matchs)

@app.route('/results/', methods=['POST'])
def results():
    results=[]
    for i in range(1,Nbr_player+1) :
        results.append(request.form['match{}'.format(i)])
    #On utilise le template accueil.html, avec les variables titre et lignes
    return render_template('results.html.j2', nbr_player=Nbr_player, type_tournoi=Type_tournoi)

if __name__ == '__main__' :
    app.run(debug=True) #, host='192.168.1.91', port=int("443")
