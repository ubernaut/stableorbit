#Server code sxr_server.py
import SimpleXMLRPCServer
import orbitSystem
#import GeneticAlgorithm
class StringFunctions(object):
    def __init__(self):
        self.seedcount = 1
        self.population = []
    def getRandomSeed(self):
        self.seedcount+=1
        return self.seedcount
    def getTimeSteps(self):
        return 100
    def getGoalFitness(self):
        return -0.3
    def getInstructions(self, fitness):
        if ((fitness<20)&(fitness>-10)):
            return "mutate"
        elif((fitness<2)&(fitness>-2)):
            return "goal"            
        else:
            return "regenerate"
        

if __name__=='__main__':
    server = SimpleXMLRPCServer.SimpleXMLRPCServer(("localhost", 8000))
    server.register_instance(StringFunctions())
    server.register_function(lambda astr: '_' + asts, '_string')
    server.serve_forever()
    
