import random
import dircache
import random
import math
import sys
import os
import copy
import StarSystem
from StarSystem import StarSystem

class Wave(object):
    def __init__(self, vel, lam):
        self.freq = vel/lam      
        return
    def setInt(self, inten, dist):
        self.energy = inten*dist
        return
    def getLamForVel(self, newVel):
        return (newVel/self.freq)
    def getVelForLam(self, newLam):
        return (self.freq * newLam)
    def getIntForD(self, newdist):
        return (self.energy / (4*3.14)*newdist*newdist)
    
class Physics(object):
    def __init__(self):
        print "Physics Loaded"
        return
    
