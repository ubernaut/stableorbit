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
		self.array=[self.x,self.y,self.z]
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
		self.temp=0.0
	
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
                self.body = Body()
                if matbodies==[]:
                        matbodies = []
                        self.matbodies.append(Body())
                else:
                        self.matbodies = matbodies  

                        
                        
class Star(object):
        def __init__(self, xPos=0, yPos=0, zPos=0, aName="default"):#, matquants[]):#, seed=0):
##                random.seed(0)
##                self.matquants=[]
##                if (False):
##                        self.matquants.append(random.uniform(1,2)) #iron
##                        self.matquants.append(random.uniform(matquants[0],(2*matquants[0])))#minerals
##                        self.matquants.append(random.uniform(matquants[1],(2*matquants[1])))#hydrogen compounds        
##                        self.matquants.append(random.uniform(matquants[2],(2*matquants[2])))#helium
##                        self.matquants.append(100-(matquants[0]+matquants[1]+matquants[2]))#hydrogen
                self.body = Body(["star",1,xPos,yPos,zPos,0,0,0,0,0,0])
##                self.matbodies=[]#matbodies
                self.buildrandom()
                self.body.name = aName
                #self.body.color = [0.0,0.0,1.0]
                #self.body.mass = self.mass
                #self.radius = self.radius
                #self.player = Player()
        def buildrandom(self):
                starrand = random.uniform(1,10000)
                if (starrand < 7600):
                        self.mtype()
                if (starrand < 8800  and starrand > 7600):
                        self.ktype()
                if (starrand < 9400 and starrand > 8800):
                        self.gtype()
                if (starrand < 9700 and starrand > 9400):
                        self.ftype()
                if (starrand < 9800 and starrand > 9900):
                        self.atype()
                if (starrand < 9900 and starrand > 9950):
                        self.btype()
                if (starrand > 9950):
                        self.otype()
        def otype(self):
                self.body.color = [0.0,0.0,1.0]
#                self.body.color = [0.0,0.0,1.0,1.0]
                self.body.mass = 16
                self.body.radius = 6.6
                self.body.temp= 33000
                self.body.type="o"
        def btype(self):
                self.body.color = [0.5,0.5,0.8,1.0]
                #self.body.color = [1.0,0.0,0.0]
                self.body.mass = 2.1
                self.body.radius = 1.8
                self.body.temp= 10,000
                self.body.type="b"
        def atype(self):
                self.body.color = [1.0,1.0,1.0,1.0]
               #self.body.color = [1.0,0.0,0.0]
                self.body.mass = 1.4
                self.body.radius = 1.4
                self.body.temp= 7500
                self.body.type="a"
        def ftype(self):
                self.body.color = [1.0,1.0,0.8,1.0]
                self.body.color = [1.0,0.0,0.0]
                self.body.mass = 1
                self.body.radius = 1
                self.body.temp= 6000
                self.body.type="f"
        def gtype(self):
#                self.body.color = [1.0,0.0,0.0]
                self.body.color = [1.0,1.0,0.0,1.0]
                self.body.mass = .8
                self.body.radius = 0.9
                self.body.temp= 5200
                self.body.type="g"
                self.body.tex=""
        def ktype(self):
                #self.body.color = [1.0,0.0,0.0]
                self.body.color = [1.0,0.2,0.2,1.0]
                self.body.mass = .7
                self.body.radius = 0.5
                self.body.temp= 3700
                self.body.type="k"
        def mtype(self):
                self.body.color = [1.0,0.0,0.0,1.0]
                #self.body.color = [1.0,0.0,0.0]
                self.body.mass = .2
                self.body.radius = .2
                self.body.temp= 2000
                self.body.type="m"
                    

            
class StarSystem(object):
                    
        def __init__(self,arg="Random"):
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
                        self.buildSol()
                if(arg=="Random"):
                        self.genSys()
                if(arg=="fromStar"):
                        return
                return
        
                        

        def genFromStar(self, star):
                self.stars=[]
                self.stars.append(star)
                self.body =star.body
                self.name = "star"#star.name
                
        def genSys(self, star=Star()):
                self.stars.append(star)
                
            
        def buildSol(self):
                sol = Star()
                sol.gtype()
                sol.mass =1
                sol.radius = .0093
                sol.body=Body(["Sol",1,0,0,0,0,0,0,0,0,0])
                self.stars.append(sol)
                earth = Planetoid([Body(["Earth",0.000003,1,0,0,0,0,0,0,0,0])])
                earth.matbodies[0].radius=0.000042
                                  
                      
class Galaxy(object):
        def __init__(self):
                self.starsystems = []
                self.theta = 0
                self.dTheta = .05
                self.maxTheta = 10
                self.alpha = 2000
                self.beta = 0.25               
                self.e = 2.71828182845904523536
                self.starDensity = 10
                while self.theta< self.maxTheta:
                        self.theta+=self.dTheta
                        randRange = 2000/(1+self.theta/2)
                        self.starDensity = int(round(10/(1+self.theta/2)))
                        for i in range(0,self.starDensity):
                                xPos = self.alpha*(self.e**(self.beta*self.theta))*math.cos(self.theta)
                                yPos = self.alpha*(self.e**(self.beta*self.theta))*math.sin(self.theta)
                                xPos+=random.uniform(-randRange,randRange)
                                yPos+=random.uniform(-randRange,randRange)
                                zPos = random.uniform(-randRange,randRange)
                                
                                newStarSys=StarSystem("fromStar")
                                newStarSys.genFromStar(Star(xPos,yPos,zPos, i))
                                newStarSys2=StarSystem("fromStar")
                                newStarSys2.genFromStar(Star(-xPos,-yPos,-zPos, -i))                                                       
                                self.starsystems.append(newStarSys)
                                self.starsystems.append(newStarSys2)
                self.localSystem = self.starsystems[0]

