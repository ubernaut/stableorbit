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
    def __init__(self, xString = 'http://192.168.1.106:8000', 
scoreThresh=1):
        self.server = xmlrpclib.Server(xString)
        self.xfile = self.server.getSystem()
        self.mySystem = cPickle.loads(self.xfile)
        self.Evaluator = Eval(self.mySystem, 1000)
        self.scoreThreshold =scoreThresh;
        self.score = 1000
        while self.score > self.scoreThreshold:
            self.xfile = self.server.getSystem()
            self.mySystem = cPickle.loads(self.xfile)
            self.Evaluator = Eval(self.mySystem, 1000)
            self.score = self.Evaluator.evaluate()
            print self.score
        self.server.insertSystem(self.xfile)
        self.planetWindow = Universe(self.Evaluator)
        run()

defaultClient = solarClient()
