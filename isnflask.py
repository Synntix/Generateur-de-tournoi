#! python3
# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, request
app = Flask(__name__)   # Initialise l'application Flask

@app.route('/')  # C'est un décorateur, on donne la route ici "/"  l'adresse sera donc localhost:5000/
def accueil():
    return render_template("accueil.html.j2", titre="Accueil") # On utilise le template accueil.html, avec les variables titre et lignes

@app.route('/player_entry/', methods=['POST'])
def player_entry():
    global Nbr_player
    global Type_tournoi
    Nbr_player=int(request.form['nbr_player'])
    Type_tournoi=request.form['type_tournoi']
    return render_template('page2.html.j2' , nbr_player=Nbr_player, type_tournoi=Type_tournoi)

@app.route('/display/', methods=['POST'])
def display():
    global Players
    Players=[]
    for i in range(1,Nbr_player+1) :
        Players.append(request.form['pseudo{}'.format(i)])
    print(Players)
    return render_template('display.html.j2' , players=Players ,nbr_player=Nbr_player, type_tournoi=Type_tournoi)

@app.route('/results/', methods=['POST'])
def results():
    return render_template('results.html.j2', nbr_player=Nbr_player, type_tournoi=Type_tournoi)

if __name__ == '__main__' :
    app.run(debug=True) #, host='192.168.1.91', port=int("443")
