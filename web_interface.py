#! python3
# -*- coding: utf-8 -*-
#title           :web_interface.py
#description     :Ce programme lance le serveur web du projet
#author          :Synntix
#date            :12/05/2019
#python_version  :3.7
#=======================================================================
from flask import Flask, render_template, url_for, request, session
import time
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
import reportlab.lib.styles
import reportlab.lib.colors
from reportlab.lib.colors import HexColor
from copy import deepcopy
import sqlite3
import tournament
import tournoi_DB
app = Flask(__name__)   # Initialise l'application Flask
debug=True
debug_algo=True

app.secret_key = 'TournoiAJE'


@app.route('/')  #On donne la route ici "/"  l'adresse sera donc localhost:5000/
def accueil():
    #On utilise le template accueil.html
    return render_template("accueil.html.j2")




@app.route('/donnees')  #On donne la route ici "/"  l'adresse sera donc localhost:5000/
def donnees():
    #On utilise le template donnees.html
    return render_template("donnees.html")




@app.route('/player_entry/', methods=['POST'])
def player_entry():
    #On récupère les réponses des formulaires de la page d'accueil
    session['Nbr_player'] = int(request.form['nbr_player'])
    session['Type_tournoi']=request.form['type_tournoi']
    session['Pts_win']=int(request.form['pts_win'])
    session['Pts_draw']=int(request.form['pts_draw'])
    session['Pts_lose']=int(request.form['pts_lose'])

    if debug==True:
        print("Nombre de joueurs : {}".format(session['Nbr_player']))
        print("Type de tournoi : {}".format(session['Type_tournoi']))
        print("Nombre de points par match gagné : {}".format(session['Pts_win']))
        print("Nombre de points par égalité : {}".format(session['Pts_draw']))
        print("Nombre de points par match perdu : {}".format(session['Pts_lose']))

    #On utilise le template page2.html
    return render_template('page2.html.j2' , nbr_player=session['Nbr_player'], type_tournoi=session['Type_tournoi'])




@app.route('/display/', methods=['POST'])
def display():
    #On crée la liste 'Players' et on ajoute tous les pseudo des participants
    session['Players']=[]
    for i in range(1,session['Nbr_player']+1) :
        #On ajoute le pseudo des joueurs à la liste "Players"
        session['Players'].append(request.form['pseudo{}'.format(i)])
    if debug==True:
        print("Liste des joueurs :\n{}".format(session['Players']))

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
    Matchlist=tournament.getMatchList(session['Nbr_player'],Extended,False,debug_algo)
    session['Matchlist']=Matchlist
    if debug==True:
        print("Liste des matchs par ID :\n{}".format(Matchlist))
    session['Nbr_matchs'] = len(Matchlist)

    #On crée les tables de la base de donnée
    tournoi_DB.openDB()
    tournoi_DB.createTables()
    #On donne la liste des joueurs à la base de donnée
    tournoi_DB.createPlayers(session['Players'])

    #On crée une liste des matchs avec le pseudo des joueurs au lieu de leur IDs
    Matchlist_pseudo=deepcopy(Matchlist)
    for i in range(len(Matchlist_pseudo)):
        Matchlist_pseudo[i]=list(Matchlist_pseudo[i])
    for i in Matchlist_pseudo:
        i[1]=tournoi_DB.getPseudo(i[1])
        i[2]=tournoi_DB.getPseudo(i[2])
    if debug==True:
        print("Liste des matchs par pseudo : \n{}".format(Matchlist_pseudo))

    #On utilise le template display.html
    return render_template('display.html.j2' , players=session['Players'] ,nbr_player=session['Nbr_player'], type_tournoi=session['Type_tournoi'], matchlist=Matchlist, matchlist_pseudo=Matchlist_pseudo, nbr_matchs=session['Nbr_matchs'])




@app.route('/results/', methods=['POST'])
def results():
    results=[]
    for i in range(1,session['Nbr_matchs']+1) :
        #On récupère l'id des joueurs qui ont gagné pour les mettre dans la liste results
        results.append(int(request.form['match{}'.format(i)]))
    if debug==True:
        print("Liste des IDs des gagnants (0 = égalité) : \n{}".format(results))

    #On récupère le classement et le convertit en classement_pseudo qui contient les pseudos
    session['Classement_pseudo']=tournament.getClassement(session['Nbr_player'],session['Matchlist'],results,session['Pts_win'],session['Pts_draw'],session['Pts_lose'],debug_algo)
    for i in range(len(session['Classement_pseudo'])):
        session['Classement_pseudo'][i]=list(session['Classement_pseudo'][i])
    for i in range(len(session['Classement_pseudo'])):
        session['Classement_pseudo'][i][0]=(tournoi_DB.getPseudo(session['Classement_pseudo'][i][0]))
    if debug==True:
        print("Classement_pseudo : {}".format(session['Classement_pseudo']))

    #Création du compte rendu en pdf avec le module reportlab
    doc = SimpleDocTemplate("Résultats-tournoi.pdf",pagesize=letter,rightMargin=60,leftMargin=60,topMargin=60,bottomMargin=18,BackColor=reportlab.lib.colors.yellow)

    Story=[]

    styles=reportlab.lib.styles.getSampleStyleSheet()
    styles.add(reportlab.lib.styles.ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles.add(reportlab.lib.styles.ParagraphStyle(name='Center', alignment=TA_CENTER))
    styles.add(reportlab.lib.styles.ParagraphStyle(name='Premier',textColor=reportlab.lib.colors.red))
    styles.add(reportlab.lib.styles.ParagraphStyle(name='Deuxieme',textColor=reportlab.lib.colors.orange))
    styles.add(reportlab.lib.styles.ParagraphStyle(name='Troisieme',textColor=reportlab.lib.colors.brown))

    localtime = time.localtime(time.time())
    date=time.strftime('%d-%m-%Y', localtime)
    heure=time.strftime('%H:%M', localtime)

    titre_pdf="{0} de {1} joueurs le {2} à {3}".format(session['Type_tournoi'],session['Nbr_player'],date,heure)
    ptext = '<font size=12>%s</font>' % titre_pdf
    Story.append(Paragraph(ptext, styles["Center"]))

    Story.append(Spacer(1, 12))

    for i in range (0,session['Nbr_player']):
        ptext = "<font size=12>{0}.    {1} avec {2} points.</font>".format(i+1,session['Classement_pseudo'][i][0][0][0],session['Classement_pseudo'][i][1])
        if i == 0:
            Story.append(Paragraph(ptext, styles["Premier"]))
        elif i == 1 :
            Story.append(Paragraph(ptext, styles["Deuxieme"]))
        elif i == 2 :
            Story.append(Paragraph(ptext, styles["Troisieme"]))
        else:
            Story.append(Paragraph(ptext, styles["Normal"]))

    print(Story)
    curr_dir=os.getcwd()
    os.chdir(curr_dir+'/static')
    doc.build(Story)
    os.chdir(curr_dir)

    #On utilise le template results.html
    return render_template('results.html.j2', nbr_player=session['Nbr_player'], type_tournoi=session['Type_tournoi'], classement_pseudo=session['Classement_pseudo'])




if __name__ == '__main__' :
    app.run(debug=True)
