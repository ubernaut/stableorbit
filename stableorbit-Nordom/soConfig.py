import os
import cPickle
import sys
import datetime
import soSession

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
            playerName="Default"#raw_input()
            self.configs.append(
                soConfigEntry("pandafig", ["fullscreen 0","win-size 1200 600"]))
            self.configs.append(
                soConfigEntry("clientRole", True))
            self.configs.append(
                soConfigEntry("maxBodyCount", 15))
            self.configs.append(
                soConfigEntry("offline", True))
            self.saveConfig()
    def setConfig(self, newEntry):
        for entry in self.configs:
            if entry.name == newEntry.name:
                self.configs.remove(entry)
        self.configs.append(newEntry)
    def getConfig(self, entryName):
        print "retrieving config option: ", entryName
        for entry in self.configs:
            if entry.name == entryName:
                return entry.value
            else:
                print "no config entry for ", entry.name
                return None
                 
    def loadConfig(self):
        print os.listdir("./")
        print "loading config ", self.name
        try:
            savefile=open(self.name).read()
            self = cPickle.loads(savefile)
            #savefile.close()            
        except:
            print "couldn't load", self.name
            
    def saveConfig(self):
        print"saving config file: ", self.name
        configFile = cPickle.dumps(self)
        saveFile = open(self.name, "w+")
        saveFile.write(configFile)
        saveFile.close()
