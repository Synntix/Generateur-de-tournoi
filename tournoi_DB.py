import sqlite3
import web_interface
import tournament

#def main():


    #openDB()
    #createTables()

    #testPlayers = ["Alain","Julien", "Alex", "Eliott"]

    #createPlayers(testPlayers)

    #resPlayer = getPlayers()

    #for i in range(len(resPlayer)):
        #print(resPlayer[i])

    #testIds = [4]

    #resPseudo= getPseudo(testIds)

    #for i in range(len(resPseudo)):
        #print(resPseudo[i])
    #n = 4
    #listmatch = tournament.getMatchList(n)
    #print(listmatch)
    #creatematch(listmatch)
    #vainq =isnflask.results()
    #createVictoire(vainq)
    #testVictoire = [2,3,4]

    #upVictoire(testVictoire)


    #closeDB()

 # SCRUD
 # SEARCH


def getPlayers():

    players = curseur.execute("SELECT id FROM joueurs ").fetchall()

    return players


def getPseudo(pIds):

    connexion = sqlite3.connect("tournoi.sqlite3", check_same_thread=False)
    curseur = connexion.cursor()
    pseudo = curseur.execute('SELECT pseudo FROM joueurs WHERE id={}'.format(pIds)).fetchall()

    return pseudo[0][0]

# CREATE
def openDB():
    global connexion
    connexion = sqlite3.connect("tournoi.sqlite3", check_same_thread=False)

def closeDB():
    connexion.close()


def createTables():
    global curseur

    curseur = connexion.cursor()

    curseur.executescript('''DROP TABLE IF EXISTS joueurs;

        CREATE TABLE IF NOT EXISTS joueurs(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        pseudo TEXT,
        victoire INTEGER,
        defaite INTEGER,
        egalite INTEGER);''')

    curseur.executescript('''DROP TABLE IF EXISTS match;

        CREATE TABLE IF NOT EXISTS match(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        round INTEGER,
        joueur1 INTEGER,
        joueur2 INTEGER,
        score_j1 INTEGER,
        score_j2 INTEGER,
        vainqueur INTEGER);''')


def createPlayers(Players_list):

    for Pseudo in Players_list:
        curseur.execute("INSERT INTO joueurs (pseudo) VALUES ('{}')".format(Pseudo))

    connexion.commit()

def creatematch(listmatch):
    curseur.executemany('INSERT INTO match (round,joueur1,joueur2) VALUES (?,?,?)',listmatch)
    connexion.commit()

def insertScore(Score_per_match):
    connexion = sqlite3.connect("tournoi.sqlite3", check_same_thread=False)
    curseur = connexion.cursor()
    for i in range(0,len(Score_per_match)) :
        curseur.execute('UPDATE match SET score_j1={0},score_j2={1} WHERE id={2}'.format(Score_per_match[i][0],Score_per_match[i][1],i+1))
    connexion.commit()

def insertWinner(Results_pseudo):
    connexion = sqlite3.connect("tournoi.sqlite3", check_same_thread=False)
    curseur = connexion.cursor()
    for i in range(0,len(Results_pseudo)) :
        curseur.execute("UPDATE match SET vainqueur='{}' WHERE id={}".format(Results_pseudo[i],i+1))
    connexion.commit()

##def createVictoire(vainq):
    ##curseur.executemany('INSERT INTO match (vainqueur) VALUES (?)',vainq)
    ##connexion.commit()
# READ

# UPDATE
#def upVictoire(pVictoire):
    #curseur.execute('UPDATE joueurs SET victoire = (?) WHERE id=1 ',pVictoire)

    #connexion.commit()
# DELETE


if __name__ == '__main__':
    import sys
    sys.exit()
#main()
