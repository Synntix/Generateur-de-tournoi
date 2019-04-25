import sqlite3
import isnflask


#def main():

  #  openDB()
  #  createTables()

   # testPlayers = ["Alain","Julien", "Alex", "Eliott"]
    
   # createPlayers(testPlayers)

  #  resPlayer = getPlayers()
    
  #  for i in range(len(resPlayer)):
   #     print(resPlayer[i])

   # testIds = [4,2]
    
   # resPseudo= getPseudo(testIds)
    
    #for i in range(len(resPseudo)):
       # print(resPseudo[i])

    #closeDB()

# SCRUD
# SEARCH


def getPlayers():

    players = curseur.execute("SELECT id FROM scores ").fetchall()

    return players


def getPseudo(pIds):

    # tupleIds = ""
    # for i in range(len(pIds)):
    #     tupleIds += str(pIds[i]) + ","

    questionmarks = '?' * len(pIds)
    formatted_query = 'SELECT pseudo FROM scores WHERE id in ({})'.format(','.join(questionmarks))
    pseudos = curseur.execute(formatted_query, pIds).fetchall()

    return pseudos

# CREATE
def openDB():
    global connexion
    connexion = sqlite3.connect("tournoi.sqlite3")

def closeDB():
    connexion.close()


def createTables():
    global curseur

    curseur = connexion.cursor()

    curseur.executescript('''DROP TABLE IF EXISTS scores;
    
        CREATE TABLE IF NOT EXISTS scores(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        pseudo TEXT,
        victoire INTEGER,
        defaite INTEGER);''')

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

    curseur.executemany('INSERT INTO scores (pseudo) VALUES (?)', tuplePlayers)

    connexion.commit()

# READ

# UPDATE

# DELETE


if __name__ == '__main__':
    import sys
#    sys.exit(main(sys.argv))
    main()
