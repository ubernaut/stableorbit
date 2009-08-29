import xmlrpclib
import orbitSystem
import Eval
import cPickle
from orbitSystem import Body
from orbitSystem import System
from orbitSystem import Galaxy
from Eval import soPhysics

class solarClient(object):
    def __init__(self, xString='http://bamdastard.kicks-ass.net:8000',
                 mode="normal", userName="Default"):
        self.connected=False
        self.xString = xString
        self.username = userName
        self.sysName = "aSystem"
        self.mode = mode
        self.scoreThreshold = 1;
        self.score = 1000
        self.galaxy = Galaxy()
        if xString == "local":
            self.runLocal()

    def clientLoop(self):
        try:
#            self.retrieveGalaxy()
#            self.logIn()
            self.generateSystem()
#            self.insertSystem()
            self.launchSystem()
        except:
            self.runLocal()
            
    def logIn(self):
        print"Please type your username and password"
        print "user: "
        uname = raw_input()
        if uname=="":
            uname="Default"
        print "pass: "
        passw = raw_input()
        self.connectToServer()
        self.Player=self.server.playerLogin(uname, passw)

    def insertSystem(self):
        self.xfile=cPickle.dumps(self.mySystem)
        if(self.connected == False):
            self.connectToServer()
        self.sysName = self.server.insertSystem(self.xfile)
        print self.sysName
        
    def getMyStars(self):
        print "getting all star names"
        allStars = self.server.getAllStars()
        for star in allStars:
            print star
        return

    def connectToServer(self):
        print "connecting to server ",self.xString
        self.server = xmlrpclib.Server(self.xString)
        self.connected=True
        
    def retrieveGalaxy(self):
        if self.connected == False:
            self.connectToServer()
        print "retrieving galaxy"
        xfile = self.server.getGalaxy()
        print "loading galaxy"
        self.galaxy=cPickle.loads(xfile)

    def retrieveSystem(self):
        if self.connected == False:
            self.connectToServer()        
        #self.getAllStars()
        print "attempting to retrieve and launch system: "
        print self.sysName
        self.xfile = self.server.retrieveSystem(self.sysName)
        print "unpacking system"
        self.mySystem = cPickle.loads(self.xfile)
        print "launching evaluator"
        self.Evaluator = Eval(self.mySystem, 1000)
        print "calculating score"
        self.score = self.Evaluator.evaluate()
        print "system stability score = "
        print self.score
        print "launching planetarium.. .  .    .        ."
        import planetarium
        self.planetWindow = planetarium.Universe(self.Evaluator)
        run()
        
    def runSol(self):
        print "earthSun"
        sysCount = 0
        self.mySystem = System(sysCount)
        self.Evaluator = soPhysics(self.mySystem, 100,0.2)
        print "number of bodies:"
        print len(self.mySystem.bodies)
        print "launching planetarium.. .  .    .        ."
        import planetarium
        self.planetWindow = planetarium.Universe(self.Evaluator)
        run()

    def generateSystem(self):
        sysCount = 1
        self.mySystem = System(sysCount)
        self.scoreThreshold =1;
        self.score = 1000
        starcount=1
        bodycount = 50
        bodyDistance=3
        bodySpeed=0.1
        self.mySystem = System(sysCount, starcount,
                               bodycount, bodyDistance,
                               bodySpeed)
        try:
            print "trying to get a star"
            self.connectToServer()
            self.mySystem.star = cPickle.loads(self.server.getNextStar())
            print "got one"
            
        except:
            print "couldn't get one"
            self.galaxy.stars[4*len(self.galaxy.stars)/5] 
        self.Evaluator = soPhysics(self.mySystem, 10000, .02)
        print "number of bodies:"
        print len(self.mySystem.bodies)
        
    def launchSystem(self):
        print "launching planetarium.. .  .    .        ."
        import planetarium        
        import interactiveConsole.interactiveConsole
        from interactiveConsole.interactiveConsole import(
            pandaConsole, INPUT_CONSOLE, INPUT_GUI,
            OUTPUT_PYTHON, OUTPUT_IRC)
        
        self.console = pandaConsole( INPUT_CONSOLE|INPUT_GUI
                                     |OUTPUT_PYTHON|OUTPUT_IRC,
                                     locals() )
        self.planetWindow = planetarium.Universe(self.Evaluator,
                                                 self.galaxy.stars,
                                                 self.console)
        run()
        
    def runLocal(self):
        print "run sol? y/n"
        genvar = 'n'#raw_input()
        if genvar == 'y':
            self.runSol()
        else:
            self.generateSystem()
        self.launchSystem() 

#Uncomment the following line to retrieve "system6" from the server
#defaultClient = solarClient('http://bamdastard.kicks-ass.net:8000', 1, "system20.sys")
#Uncomment the following line if you want the client to run offline
#defaultClient = solarClient("local")
#defaultClient = solarClient("runSol")
#This is the default configuration which attempts to retrieve a system from
#the server. Failure will cause the client to launch locally in disconnected mode
#defaultClient = solarClient("192.168.0.101:8000", "normal")
#defaultClient = solarClient()
#defaultClient.clientLoop()
