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
server = xmlrpclib.Server('http://localhost:8000')
xfile = server.getSystem()
mySystem = cPickle.loads(xfile)
print xfile
Evaluator = Eval(mySystem, 1000)
planetWindow = Universe(Evaluator)
run()
