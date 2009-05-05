#Server code solarClient
import orbitSystem
import cPickle
import SimpleXMLRPCServer
import sys
#sys.path.append('./beta')
#import StableOrbitDAO

import os
from orbitSystem import System

class solarServer(object):
    def __init__(self,xString):
        import string
        print "solarServer launched: "+xString+":8000"
        self.python_string = string
        self.seedcount = 1
        
    def getSystem(self):
        print "recieved system request"
        self.seedcount += 1
        aSystem = orbitSystem.System(self.seedcount)
        aString = cPickle.dumps(aSystem)
        print "sending system"
        return aString
        #xfile = open("serialSystem.txt")
        #print xfile.read()
    def insertSystem(self, xfile):# playerName, fitness, iterations):
        print"connection acquired"
        os.chdir('data')
        sysName = 'system'+str(self.seedcount)+'.sys'
        print "saving system as:"
        print sysName
        saveFile = open(sysName, "w+")
        saveFile.write(xfile)
        saveFile.close()
        os.chdir("..")
        return sysName
    def retrieveSystem(self, sysName):
        print "recieved request to retrieve system"
        print sysName
        os.chdir('data')
        xfile = open(sysName).read()
        os.chdir("..")
        print "sending system"
        return xfile
        #print xfile
        #StableOrbitDAO.insertSystem(xfile)
  
if __name__=='__main__':
    xString = "192.168.1.100"
#    xString = "localhost"
    server = SimpleXMLRPCServer.SimpleXMLRPCServer((xString, 8000))
    server.register_instance(solarServer(xString))
    server.serve_forever()
    
