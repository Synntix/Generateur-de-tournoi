import sqlite3
import isnflask

    

def main():
    global connexion
    global curseur
    connexion = sqlite3.connect("tournoi.sqlite3")
    
    
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
        round INTEGER?
        joueur1 INTEGER,
        joueur2 INTEGER,
        vainqueur INTEGER);''')

   
def getid(Players):

    for i in range(len(Players)) :
        Players[i]=(Players[i],)
    
    #Exécutions multiples
    curseur.executemany('INSERT INTO scores (pseudo) VALUES (?)', Players)
    
    connexion.commit()  #Ne pas oublier de valider les modifications
    
    id=curseur.execute("SELECT id FROM scores ").fetchall()
    
    return id
        
        
def getPseudo(result):
    
    Pseudo=curseur.execute('SELECT pseudo FROM scores WHERE id = ?',result).fetchall()
    
    return Pseudo

    connexion.close()
    
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))




