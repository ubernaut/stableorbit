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
aSolarSystem.buildPrime(seedNumber)
Evaluator = Eval(aSolarSystem, timeStepCount)
print "Current system fitness:"
systemFitness = Evaluator.evaluate()
print systemFitness

while (server.getInstructions(systemFitness)=="regenerate"):
    print "regenerating system"
    seedNumber = server.getRandomSeed()
    print "new seed:"
    print seedNumber
    aSolarSystem = System(seedNumber)
    #aSolarSystem.buildPrime(seedNumber)
    Evaluator = Eval(aSolarSystem, timeStepCount)
    print "Current system fitness:"
    systemFitness = Evaluator.evaluate()
    print systemFitness
    
print "acceptable system found"
    
#TODO return completed system back to the server

planetWindow = Universe()
planetWindow.importSystem(aSolarSystem)
planetWindow.loadPlanets()
run()
