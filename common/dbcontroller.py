"""File for handling the database"""

import sqlite3
from pathlib import Path

# DBSTORAGE: str = str(Path('ressources/appDB.db').resolve())
DBSTORAGE: str = str(Path('../data/appDB.db').resolve())


class DbEngine:

    def requestDB(self, requete):
        con = sqlite3.connect(DBSTORAGE)
        mycursor = con.cursor()


        mycursor.execute(requete)

        # Save(commit) changes
        con.commit()
        con.close()
        return True

    def selectDB(self, requete):
        con = sqlite3.connect(DBSTORAGE)
        mycursor = con.cursor()

        mycursor.execute(requete)
        resultat = mycursor.fetchall()
        con.close()
        return resultat


if __name__=='__main__':
    print(DBSTORAGE)
    con = DbEngine()
    res = con.selectDB(" select cryptopair,basecoin,quotecoin from relationalcoin")
    data ={name: f'{bsc}-{qtc}' for name,bsc,qtc in res}
    print(data)

    

