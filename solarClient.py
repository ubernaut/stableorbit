#Client code sxrclient.py
import xmlrpclib
import orbitSystem
import planetarium
import Eval
import cPickle
from planetarium import Universe
from orbitSystem import Body
from orbitSystem import System
#import psyco
#psyco.full()
from Eval import Eval

class solarClient(object):
    def __init__(self, xString='http://bamdastard.kicks-ass.net:8000', scoreThresh=1):
        if xString == "standalone":
                runLocal()
       # for (i=0;i<10;i++):   
        try:
            print "connecting to server "+xString
            self.server = xmlrpclib.Server(xString)
            print "connection acquired"
            self.scoreThreshold =scoreThresh;
            self.score = 1000
            while self.score > self.scoreThreshold:
                print "retrieving a system"
                self.xfile = self.server.getSystem()
                print "converting xfile"
                self.mySystem = cPickle.loads(self.xfile)
                print "launching evaluator"
                self.Evaluator = Eval(self.mySystem, 1000)
                print "calculating score"
                self.score = self.Evaluator.evaluate()
                print "system stability score = "+self.score
            print"found acceptable system"
            self.server.insertSystem(self.xfile)
            print self.server.retrieveSystem("test request")
            self.planetWindow = Universe(self.Evaluator)
            run()
        except:
            print "oops, there was an error"
            #self.runLocal()
      
    def runLocal(self):
        print "unable to connect to server"
        sysCount = 1
        self.mySystem = System(sysCount)
        self.Evaluator = Eval(self.mySystem, 1000)
        self.scoreThreshold =1;
        self.score = 1000
        while self.score > self.scoreThreshold:
            self.mySystem = System(sysCount)
            self.Evaluator = Eval(self.mySystem, 1000)
            self.score = self.Evaluator.evaluate()
            print "system stability score = "+self.score
            sysCount+=1
        self.planetWindow = Universe(self.Evaluator)
        run()

defaultClient = solarClient("192.168.1.101:8000", 1)
#defaultClient = solarClient("127.0.0.1:8000", 1)
#defaultClient = solarClient("localhost:8000", 1)
#defaultClient = solarClient()

