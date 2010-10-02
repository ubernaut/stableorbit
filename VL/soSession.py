import StarSystem
#import solarClient
#from solarClient import solarClient
#import solarServer
import os
import cPickle
import sys
import datetime
#import SoCore
#from SoCore import SoCore

#import soConfig
#from soConfig import soConfigEntry

from pandac.PandaModules import loadPrcFileData
        
class soPlayer(object):
    def __init__(self, name="Default", password="Default",
                 inip="127.0.0.1", exip="127.0.0.1"):
        self.name = name
        self.password = password
        self.internalip = inip
        self.externalip = exip
        self.online = False
        self.visitedStars = []
        self.lastOnline = datetime.datetime.now()
        self.health =100

class soSession(object):
    def __init__(self, args=["fullscreen 0","win-size 1300 800",
                             "sofig-blank", "sofig-noconsole",
                             "sofig-noshaders", "sofig-bodycount 32"]):
        print "Creating Session"
        #self.config = soConfig(configName)
        self.pandaFigs=args
        #self.loadSession()
        self.configPanda()
        self.launchSystem()
    def loadSession(self):
        self.client = solarClient()
        self.configPanda()
        self.client.runLocal()
    def launchSystem(self):
        print "launching planetarium.. .  .    .        ."
        import SoCore        
        import interactiveConsole.interactiveConsole
        from interactiveConsole.interactiveConsole import(
            pandaConsole, INPUT_CONSOLE, INPUT_GUI,
            OUTPUT_PYTHON, OUTPUT_IRC)
        
        self.console = pandaConsole( INPUT_CONSOLE|INPUT_GUI
                                     |OUTPUT_PYTHON|OUTPUT_IRC,
                                     locals() )
        self.configPanda()
#        self.planetWindow = SoCore.SoCore(self.console)
        self.socore = SoCore.SoCore(self.console)
        run()    
    def configPanda(self):
#        figlist = self.config.getConfig("pandafig")
#        print "figs:",figlist
        for fig in self.pandaFigs:
            if not "sofig" in fig:
                loadPrcFileData("", fig)
x=soSession()
            
            
            
    
        
        
