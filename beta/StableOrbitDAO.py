from pysqlite2 import dbapi2 as sqlite
from orbitSystem import System

con = sqlite.connect("stableOrbit")

class StableOrbitDAO():
    def __init__(self, connectString="stableOrbit.db"):
        self.connStr = connectString
        self.connection = sqlite.connect(self.connStr)
        self.cursor = self.connection.cursor()

#    def insertSystem(self,  xfile):
       # self.connStr = 'stableOrbit.db'
       # self.connection = sqlite.connect(self.connStr)
       # self.cursor = self.connection.cursor()
       # self.cursor.execute('INSERT INTO solarSystems VALUES ('+xfile+')')
       # self.cursor.commit()
        
        
        
