import random
import dircache
import random
import math
import sys
import os
import copy

class Material(object):
        def __init__(self, arg=""):
                if arg == "":
                        self.metal()
                if arg == "metal":
                        self.metal()
                if arg == "mineral":
                        self.mineral()
                if arg == "hcompound":
                        self.hcompound()
                if arg == "hydrogen":
                        self.hydrogen()
                if arg == "helium":
                        self.helium()

        def metal(self):
                self.name="metal"
                self.condtemp = 1000
                self.atomicweight = 55
                self.color = [0.3,0.3,0.3,1.0]

        def mineral(self):
                self.name="mineral"
                self.condtemp = 500
                self.atomicweight = 25
                self.color = [0.0,0.5,0.5,1.0]
        def hcompound(self):
                self.name="hcompound"
                self.condtemp=150
                self.atomicweight = 10
                self.color = [0.0,1.0,0.0,1.0]
        def hydrogen(self):
                self.name = "hydrogen"
                self.condtemp = 50
                self.atomicweight = 1
                self.color = [1.0,1.0,0.0,1.0]
        def helium(self):
                self.name = "helium"
                self.condtemp = 100
                self.atomicweight = 4
                self.color = [1.0,0.0,0.0,1.0]
                
class Point(object):
        def __init__(self, position_data=[0,0,0]):
                self.x=float(position_data[0])
		self.y=float(position_data[1])
		self.z=float(position_data[2])
	def reset(self):
		self.x=0
		self.y=0
		self.z=0         
                
class Body(object):
	def __init__ (self,body_data=[]):
                if body_data == []:
                        body_data=["Sol",1,0,0,0,0,0,0,0,0,0]
		self.name=body_data[0]
		self.mass=float(body_data[1])
		self.position=Point(body_data[2:5])
		self.velocity=Point(body_data[5:8])
		self.acceleration=Point(body_data[5:8])
		self.material=Material("helium")
		self.orientation=Point()
		self.angVelocity=Point()
		self.acceleration.reset()
		self.radius=.03
		self.color = self.material.color
	
	def __del__(self):
                del self.name
                del self.mass
		del self.position
		del self.velocity
		del self.acceleration
		del self.orientation
		del self.angVelocity
		del self.radius
               
class Planetoid(object):
        def __init__(self, matbodies=[]):
                self.body = Body(body_data)
                if matbodies==[]:
                        matbodies = []
                        self.matbodies.append(Body())
                else:
                        self.matbodies = matbodies  

                        
                        
class Star(object):
        def __init__(self, xPos=0, yPos=0, zPos=0, aName="default"):
                self.body = Body(["star",1,xPos,yPos,zPos,0,0,0,0,0,0])
                self.buildrandom()
                self.name = aName
                self.color = [0.0,0.0,1.0]
                self.mass = 16
                self.radius = 6.6
                self.temp= 33000
                #self.player = Player()
        def buildrandom(self):
                starrand = random.uniform(1,10000)
                if (starrand > 7600):
                        self.mtype()
                if (starrand > 8800):
                        self.ktype()
                if (starrand > 9400):
                        self.gtype()
                if (starrand > 9700):
                        self.ftype()
                if (starrand > 9800):
                        self.atype()
                if (starrand > 9900):
                        self.btype()
                if (starrand > 9500):
                        self.otype()
                
        def otype(self):
                self.color = [1.0,0.0,0.0]
#                self.color = [0.0,0.0,1.0,1.0]
                self.mass = 16
                self.radius = 6.6
                self.temp= 33000
        def btype(self):
                self.color = [0.5,0.5,0.8,1.0]
                #self.color = [1.0,0.0,0.0]
                self.mass = 2.1
                self.radius = 1.8
                self.temp= 10,000
        def atype(self):
                self.color = [1.0,1.0,1.0,1.0]
               #self.color = [1.0,0.0,0.0]
                self.mass = 1.4
                self.radius = 1.4
                self.temp= 7500
        def ftype(self):
                self.color = [1.0,1.0,0.8,1.0]
                self.color = [1.0,0.0,0.0]
                self.mass = 1
                self.radius = 1
                self.temp= 6000
        def gtype(self):
#                self.color = [1.0,0.0,0.0]
                self.color = [1.0,1.0,0.0,1.0]
                self.mass = .8
                self.radius = 0.9
                self.temp= 5200
        def ktype(self):
                #self.color = [1.0,0.0,0.0]
                self.color = [1.0,0.2,0.2,1.0]
                self.mass = .7
                self.radius = 0.5
                self.temp= 3700
        def mtype(self):
                self.color = [1.0,0.0,0.0,1.0]
                #self.color = [1.0,0.0,0.0]
                self.mass = .2
                self.radius = .2
                self.temp= 2000

            
class StarSystem(object):
        def ___init__(self,arg="Sol"): #args should be star, and materials
                self.id = 0
                self.mass = 0
                self.stars = []
                self.planets = []
                self.belts =[]
                self.fields = []
                self.items = []
                self.galaxy = []
                self.coord = [0,0,0]
                self.players=[]
                if(arg=="Sol"):
                    self.loadSol()

        def genSys(self):
                self.stars.append(Star())
                
            
        def loadSol(self):
                self.stars.append(Planetoid([Body()]))
                      
class Galaxy(object):
        def __init__(self):
                self.stars = []
                self.theta = 0
                self.dTheta = .05
                self.maxTheta = 10
                self.alpha = 2000
                self.beta = 0.25               
                self.e = 2.71828182845904523536
                self.starDensity = 1
                while self.theta< self.maxTheta:
                        self.theta+=self.dTheta
                        randRange = 2000/(1+self.theta/2)
                        self.starDensity = 10/(1+self.theta/2)
                        for i in range(0,self.starDensity):
                                xPos = self.alpha*(self.e**(self.beta*self.theta))*math.cos(self.theta)
                                yPos = self.alpha*(self.e**(self.beta*self.theta))*math.sin(self.theta)
                                xPos+=random.uniform(-randRange,randRange)
                                yPos+=random.uniform(-randRange,randRange)
                                zPos = random.uniform(-randRange,randRange)
                                newStar = Star(xPos,yPos,zPos, i)
                                newStar2 = Star(-xPos,-yPos,-zPos, 2*i)
                                self.stars.append(newStar)
                                self.stars.append(newStar2)
