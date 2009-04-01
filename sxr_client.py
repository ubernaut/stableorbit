#Client code sxrclient.py
import xmlrpclib
import orbitSystem
import planetarium
import Eval
from planetarium import Universe
from orbitSystem import Body
from orbitSystem import System
from Eval import Eval

server = xmlrpclib.Server('http://localhost:8000')

seedNumber = server.getRandomSeed()
timeStepCount = server.getTimeSteps()
goalFitness = server.getGoalFitness()

print "seed recieved: "
print seedNumber
aSolarSystem = System(seedNumber)

aSolarSystem.buildPrime()
Evaluator = Eval(aSolarSystem, timeStepCount)
print "Current system fitness:"

planetWindow = Universe(Evaluator)

run()
