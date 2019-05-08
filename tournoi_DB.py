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

    pIds=(pIds,)

    pseudos = curseur.execute('SELECT pseudo FROM joueurs WHERE id in (?)',pIds).fetchall()

    return pseudos

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
        vainqueur INTEGER);''')


def createPlayers(pPlayers):

    tuplePlayers = []
    for i in range(len(pPlayers)):
        tuplePlayers.append((pPlayers[i],))

    curseur.executemany('INSERT INTO joueurs (pseudo) VALUES (?)', tuplePlayers)

    connexion.commit()

def creatematch(listmatch):
    curseur.executemany('INSERT INTO match (round,joueur1,joueur2) VALUES (?,?,?)',listmatch)
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
