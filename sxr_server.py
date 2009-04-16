#Server code sxr_server.py
import orbitSystem
import cPickle
import SimpleXMLRPCServer
import StableOrbitDAO
import os
from orbitSystem import System

class GalaxyServer(object):
    def __init__(self):
        import string
        self.python_string = string
        self.seedcount = 1
        
    def getSystem(self):
        self.seedcount += 1
        aSystem = orbitSystem.System(self.seedcount)
        aString = cPickle.dumps(aSystem)
        return aString
        #xfile = open("serialSystem.txt")
        #print xfile.read()
    def insertSystem(self, xfile):# playerName, fitness, iterations):
        print"connection acquired"
        print xfile
        os.chdir('data')
        saveFile = open('system'+str(self.seedcount)+'.sys', "w+")
        saveFile.write(xfile)
        saveFile.close()
        os.chdir("..")
        return True
        #print xfile
        #StableOrbitDAO.insertSystem(xfile)
  
if __name__=='__main__':
    server = SimpleXMLRPCServer.SimpleXMLRPCServer(("localhost", 8000))
    server.register_instance(GalaxyServer())
    server.serve_forever()
    
