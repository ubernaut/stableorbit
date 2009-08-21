import orbitSystem
import solarClient
import solarServer
import os
import cPickle
import sys

class soConfigEntry(object):
    def __init__(self, name="Default", value=object()):
        self.name = name
        self.value = object
class soConfig(object):
    def __init__(self, name="Default.conf", configs=[]):
        self.name = name
        self.configs=configs
        self.loadConfig()
        if self.name =="Default.conf" and self.configs == []:
            print "Creating Default.conf"
            print "please enter a player name: "
            playerName=raw_input()
            self.configs.append(
                soConfigEntry("localPlayer",soPlayer(playerName)))
            self.configs.append(
                soConfigEntry("mainScreen", ["window", "800 600"]))
            self.configs.append(
                soConfigEntry("clientRole", solarClient())
            self.configs.append(
                soConfigEntry("maxBodyCount", 15))
            self.saveConfig()
    def setConfig(self, newEntry):
        for entry in self.configs:
            if entry.name == newEntry.name:
                self.configs.remove(entry)
        self.configs.append(newEntry)
    def getConfig(self, entryName):
        for entry in self.configs:
            if entry.name == entryName:
                return entry
            else:
                print "no config entry for ", entry.name
                return None
                    
    def loadConfig(self):
        try:
            self = cPickle.loads(open(self.name))
        except:
            print "couldn't load", self.name
            
    def saveConfig(self):
        configFile = cPickle.dumps(self)
        saveFile = open(self.name, "w+")
        saveFile.write(configFile)
        saveFile.close()

        
class soPlayer(object):
    def __init__(self, name="Default", inip="127.0.0.1", exip="127.0.0.1"):
        self.name = name
        self.internalip = ip
        self.externalip = exip


class soSession(object):
    def __init__(self, configName="Default.conf", args=[]):
                self.config = soConfig(configName)
    def loadSession(self):
                clientRole = self.config.getConfig("clientRole")
                if(clientRole != None):
                    self.client = clientRole.value
                
            
            
            
    
        
        
