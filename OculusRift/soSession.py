import orbitSystem
import solarClient
from solarClient import solarClient
import solarServer
import os
import cPickle
import sys
import datetime
import soConfig
from soConfig import soConfigEntry

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
    def __init__(self, args=["fullscreen 0","win-size 1280 720",
                             "sofig-blank", "sofig-noconsole",
                             "sofig-noshaders", "sofig-bodycount 32"]):
        print "Creating Session"
        #self.config = soConfig(configName)
        self.pandaFigs=args
        self.loadSession()
    def loadSession(self):
        self.client = solarClient()
        self.configPanda()
        self.client.runLocal()
        
    def configPanda(self):
#        figlist = self.config.getConfig("pandafig")
#        print "figs:",figlist
        for fig in self.pandaFigs:
            if not "sofig" in fig:
                loadPrcFileData("", fig)
x=soSession()
            
            
            
    
        
        
