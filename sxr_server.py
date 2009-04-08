#Server code sxr_server.py
import orbitSystem
import cPickle
import SimpleXMLRPCServer
from orbitSystem import System

class GalaxyServer(object):
    def __init__(self):
        import string
        self.python_string = string
        self.seedcount = 1
    def getSystem(self):
        self.seedcount += 1
        aSystem = orbitSystem.System(self.seedcount)
        aSystem.buildPrime()
        aString = cPickle.dumps(aSystem)
        return aString
        #xfile = open("serialSystem.txt")
        #print xfile.read()
  
if __name__=='__main__':
    server = SimpleXMLRPCServer.SimpleXMLRPCServer(("localhost", 8000))
    server.register_instance(GalaxyServer())
    server.serve_forever()
    
