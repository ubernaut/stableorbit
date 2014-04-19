import random
import dircache
import random
import math
import sys
import os
import copy
#import Eval
#from Eval import soPhysics
#import psyco
#psyco.full()
#load from xml

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
                        slef.helium()

        def metal(self):
                self.name="metal"
                self.condtemp = 1000
                self.atomicweight = 55
        def mineral(self):
                self.name="mineral"
                self.condtemp = 500
                self.atomicweight = 25
        def hcompound(self):
                self.name="hcompound"
                self.condtemp=150
                self.atomicweight = 10
        def hydrogen(self):
                self.name = "hydrogen"
                self.condtemp = 50
                self.atomicweight = 1
        def helium(self):
                self.name = "helium"
                self.condtemp = 100
                self.atomicweight = 4
                

                
class Planetoid(object):
        def __init__(self, matbodies=[]):
                self.body = Body(body_data)
                if matbodies==[]:
                        matbodies = []
                        self.matbodies.append(Body())
                else:
                        self.matbodies = matbodies           
                
class Body(object):
	def __init__ (self,body_data=[]):
                if body_data == []:
                        body_data=["Sol",1,0,0,0,0,0,0,0,0,0]
		self.name=body_data[0]
		self.mass=float(body_data[1])
		self.position=Point(body_data[2:5])
		self.velocity=Point(body_data[5:8])
		self.acceleration=Point(body_data[5:8])
		self.material=Material("hydrogen")
		self.orientation=Point()
		self.angVelocity=Point()
		self.acceleration.reset()
		self.radius=.03
	
	def __del__(self):
                del self.name
                del self.mass
		del self.position
		del self.velocity
		del self.acceleration
		del self.orientation
		del self.angVelocity
		del self.radius
               
class Point(object):
        def __init__(self, position_data=[0,0,0]):
                self.x=float(position_data[0])
		self.y=float(position_data[1])
		self.z=float(position_data[2])
	def reset(self):
		self.x=0
		self.y=0
		self.z=0
		
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
                        
                        
class Star(object):
        def __init__(self, xPos=30000, yPos=0, zPos=0, aName="default"):
                self.body = Body(["body",1,xPos,yPos,zPos,0,0,0,0,0,0])
                self.name = aName
                #self.player = Player()
            
class StarSystem(object):
        def ___init__(self):
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
        def loadSol(self):
                self.stars.append(Planetoid([Body()]))
                
                
class System(object):
	def __init__(self, seed=0, starcount=1,
                     bodycount=1, abodyDistance=2, abodySpeed=0.05):
                random.seed = seed
                self.seed = seed
                self.star = Star()
		self.starCount=starcount
		self.bodyCount= bodycount
		self.bodies=[]
		self.bodyDistance = abodyDistance
		self.bodySpeed = abodySpeed
		if seed !=0:
                        self.build()
                else:
                        self.buildSol()
		print "bodyCount: "+`len(self.bodies)`
		self.stability = 0.5 - self.evaluate()
		self.printed=False
		self.avgStability=0.5 - self.evaluate()
	def moveToStar(self):                
                for body in self.bodies:
                        body.position.x += self.star.body.position.x
                        body.position.y += self.star.body.position.y
                        body.position.z += self.star.body.position.z
	def getStar(self, body_data):
                body_data.append(random.uniform(1,2))
                for j in range(0,2):
                        body_data.append(0.0)
                body_data.append(0.0)
		for j in range(0,2):
			body_data.append(0.0)
		body_data.append(0.0)
		return body_data

	def getSymPlanets(self):
                body_data=[]
                body_data.append("body_X")
                body_data.append(random.uniform(.000001,.01))
                #body_data.append(0.0)
                
                if quadrantVar > 0:
                        body_data.append(random.uniform(0,self.bodyDistance))
                        body_data.append(random.uniform(0,self.bodyDistance))
                        body_data.append(0.0)
                        body_data.append(random.uniform(0,self.bodySpeed))
                        body_data.append(random.uniform(-self.bodySpeed,0))
                        body_data.append(0.0)
                        
                if quadrantVar< 0:
                        body_data.append(random.uniform(-self.bodyDistance,0))
                        body_data.append(random.uniform(-self.bodyDistance,0))
                        body_data.append(0.0)
                        body_data.append(random.uniform(-self.bodySpeed,0))
                        body_data.append(random.uniform(0,self.bodySpeed))
                        body_data.append(0.0)
                
        def getDirectedPlanet(self):
                quadrantVar =1# random.uniform(-1,1)       
                body_data=[]
                body_data.append("body_X")
                body_data.append(random.uniform(.000001,.01))
                #body_data.append(0.0)
                
                if quadrantVar > 0:
                        body_data.append(random.uniform(0,self.bodyDistance))
                        body_data.append(random.uniform(0,self.bodyDistance))
                        body_data.append(random.uniform(0,self.bodyDistance/64))
                if quadrantVar< 0:
                        body_data.append(random.uniform(-self.bodyDistance,0))
                        body_data.append(random.uniform(-self.bodyDistance,0))
                        body_data.append(random.uniform(-self.bodyDistance/64,0))
                
                if quadrantVar > 0:
                        body_data.append(random.uniform(0,self.bodySpeed))
                        body_data.append(random.uniform(-self.bodySpeed,0))
                        body_data.append(random.uniform(0,self.bodySpeed/32))
                if quadrantVar < 0:
                        body_data.append(random.uniform(-self.bodySpeed,0))
                        body_data.append(random.uniform(0,self.bodySpeed))
                        body_data.append(random.uniform(-self.bodySpeed/32),0)
                
                
                
                return body_data
                
	def getPlanet(self, body_data):
#                body_data.append("body_"+len(self.bodies))
                body_data.append(random.uniform(.000001,.01))
                for j in range(0,2):
                        body_data.append(random.uniform(-self.bodyDistance,self.bodyDistance))
                body_data.append(0.0)
                for j in range(0,2):
                        body_data.append(random.uniform(-self.bodySpeed,self.bodySpeed))
                body_data.append(0.0)
                return body_data
        
		#self.fitness=self.system.evaluate()
		#self.sumFit=fitness
        def buildSol(self):
                self.bodies=[]
                body_data=["Sol",1,0,0,0,0,0,0,0,0,0]
                self.bodies.append(Body(body_data))
                body_data=["Earth",0.000003,0,1,0,.04,0,0,0,0,0]
                self.bodies.append(Body(body_data))
                #mercury data mass 3.3022 * 10**23 //kg
                #sun  = 1.9891 * 10**30 kg = 1 
                #body_data=["Mercury",]
                
                
	def build(self):
		for i in range(0,self.bodyCount):
			if i < self.starCount:
                                self.addStar()
			else:
                                self.addSinglePlanet()
	def addStar(self):
                body_data = self.getStar(["star"])
                body = Body(body_data)
                self.bodies.append(body)
        def reverseBody(self, adata):
                bdata = adata
                bdata[2]= 0 - adata[2]
                bdata[3]= 0 - adata[3]
                bdata[4]= 0 - adata[4]
                bdata[5]= 0 - adata[5]
                bdata[6]= 0 - adata[6]
                bdata[7]= 0 - adata[7]
                return bdata
                
	def addSinglePlanet(self):
                print "adding Body"
                body_data = self.getDirectedPlanet()
                aBody = Body(body_data)
                bBody = Body(self.reverseBody(body_data))
                otherBodies = []
                otherBodies.append(self.bodies[0])
                otherBodies.append(aBody)
                otherBodies.append(bBody)
                fitness = self.evaluateN(otherBodies)
                while fitness<.1 or fitness>1:
                        print "testing configuration"
                        adata = self.getDirectedPlanet()
                        aBody = Body(adata)
                        bdata = self.reverseBody(adata)
                        bBody = Body(bdata)
                        otherBodies = []
                        otherBodies.append(self.bodies[0])
                        otherBodies.append(aBody)
                        otherBodies.append(bBody)
                        fitness=self.evaluateN(otherBodies)
                self.bodies.append(aBody)
                self.bodies.append(bBody)
                return aBody
                
	def addPlanet(self):
                print "adding body"
                body_data = []
                body_data.append("body_X")
                body_data = self.getPlanet(body_data)
                aBody = Body(body_data)
                self.bodies.append(aBody)
                print "new stability"
                print self.evaluate()
                while self.evaluate()>1:
                        self.bodies.pop()
                        self.addPlanet()
                return                

	def mutate(self, alphaMass, alphaPosition, alphaVelocity):
		whichBody=random.randint(0,len(self.bodies)-1)
		oldPosition =copy.deepcopy(self.bodies[whichBody].position)
		if whichBody < self.starCount:
			self.bodies[whichBody].mass += alphaMass * random.uniform(-self.bodies[whichBody].mass/2,5)
			self.bodies[whichBody8].position.x+= alphaPosition * (random.uniform(-.000001,.000001))
			self.bodies[whichBody].velocity.x+= alphaVelocity * (random.uniform(-.000001,.000001))
			self.bodies[whichBody].position.y+= alphaPosition * (random.uniform(-.000001,.000001))
			self.bodies[whichBody].velocity.y+= alphaVelocity * (random.uniform(-.000001,.000001))
			self.bodies[whichBody].position.z+= alphaPosition * (random.uniform(-.000001,.000001))
			self.bodies[whichBody].velocity.z+= alphaVelocity * (random.uniform(-.000001,.000001))
		else:
			self.bodies[whichBody].mass += alphaMass * random.uniform(-self.bodies[whichBody].mass,1)
		if self.bodies[whichBody].mass >=15:
			self.bodies[whichBody].mass=14.99

		if self.bodies[whichBody].mass <= 0:
			self.bodies[whichBody].mass=0.1
			print "negetive mass"
		self.bodies[whichBody].position.x+= alphaPosition * (random.uniform(-5,5))
		self.bodies[whichBody].velocity.x+= alphaVelocity * (random.uniform(-1,1))
		self.bodies[whichBody].position.y+= alphaPosition * (random.uniform(-5,5))
		self.bodies[whichBody].velocity.y+= alphaVelocity * (random.uniform(-1,1))
		self.bodies[whichBody].position.z+= alphaPosition * (random.uniform(-5,5))
		self.bodies[whichBody].velocity.z+= alphaVelocity * (random.uniform(-1,1))
		if self.bodies[whichBody].position.z>=30 or self.bodies[whichBody].position.z<=-30 or self.bodies[whichBody].position.x>=30 or self.bodies[whichBody].position.x<=-30 or self.bodies[whichBody].position.x>=30 or self.bodies[whichBody].position.x<=-30:
			self.bodies[whichBody].position=oldPosition
		self.stability = self.evaluate(self.bodies)
	def evaluate(self):
		kinetic=0.0
		potential=0.0
		G=2.93558*10**-4
		for body in self.bodies:
			vel = body.velocity
			vel_sq = (vel.x**2 + vel.y**2 + vel.z**2)
			kinetic += 0.5*body.mass*vel_sq
		for i in range(0,len(self.bodies)):
			current_body=self.bodies[i]
			current_position=current_body.position
			for j in range(0,i):
				other_body=self.bodies[j]
				other_position=other_body.position
				d_x=(other_position.x-current_position.x)
				d_y=(other_position.y-current_position.y)
				d_z=(other_position.z-current_position.z)
				radius = (d_x**2 + d_y**2 + d_z**2)**(0.5)
				if radius >0 :
					potential -= G*current_body.mass*other_body.mass/radius
		try:	
			return abs(kinetic/potential)
		except:
			return 100
	def evaluateN(self, somebodies):
                tempSys = System()
                tempSys.bodies = somebodies
                tempEval = Eval.soPhysics(tempSys,1000000,.01)
                return tempEval.sumFit
                        
	def evaluateBodies(self, someBodies):
		kinetic=0.0
		potential=0.0
		G=2.93558*10**-4
		for body in someBodies:
			vel = body.velocity
			vel_sq = (vel.x**2 + vel.y**2 + vel.z**2)
			kinetic += 0.5*body.mass*vel_sq
		for i in range(0,len(someBodies)):
			current_body=someBodies[i]
			current_position=current_body.position
			for j in range(0,i):
				other_body=someBodies[j]
				other_position=other_body.position
				d_x=(other_position.x-current_position.x)
				d_y=(other_position.y-current_position.y)
				d_z=(other_position.z-current_position.z)
				radius = (d_x**2 + d_y**2 + d_z**2)**(0.5)
				if radius >0 :
					potential -= G*current_body.mass*other_body.mass/radius
		try:	
			return abs(kinetic/potential)
		except:
			return 100.0
	def bodies(self):
                return self.bodies

from ctypes import *
class cSystem(Structure):
        _fields_ = (("count", c_int),
                    ("allocated",c_int),
                    ("names", c_char*50),
                    ("mass",c_float*50),
                    ("rad",c_float*50),
                    ("pos",c_float*50*3),
                    ("ori",c_float*50*3),
                    ("vel",c_float*50*3),
                    ("acc",c_float*50*3))     
        
        
class GridSystem(object):
        def convert(data):
                tempDATA = []
                for i in data:
                        tempDATA.append([float(j) for j in i.split()])
                return array(tempDATA)

        def __init__(self, bodies=[]):
                self.count = len(bodies)
                N = self.count
                self.player=0
                self.names = [""]
                self.mass= [0.0]
                self.rad = [0.0]
                self.pos = [[0.0,0.0,0.0]]
                self.ori = [[0.0,0.0,0.0]]
                self.vel = [[0.0,0.0,0.0]]
                self.acc = [[0.0,0.0,0.0]]
                self.allocated =1
                self.collisions = []
                self.removed=[]
                for i in range (0,self.count):
                        self.addSpace()
                i = 0
                for body in bodies:
                        if body.name == "player":
                                self.player = i
                        self.insertBody(body, i)
                     
                        i+=1
                
                for i in range (0,self.count):
                        self.printBody(i)
        def getPlayerIndex(self):
                i=0
                lasti = 0
                for name in self.names:
                        if name == "player":
                                self.player = i
                                lasti=i
                                return i
                                #print "player found at ",i                                
                        else:
                                i+=1
                return i

        def append(self, body):
                print "appending: ", self.count
                print "allocated: ", self.allocated
                
        def insertBody(self,body, i):
                self.names[i] = body.name
                self.mass[i] = body.mass
                self.rad[i] = body.radius
                self.pos[i][0] = body.position.x
                self.pos[i][1] = body.position.y
                self.pos[i][2] = body.position.z

                self.ori[i][0] = body.orientation.x
                self.ori[i][1] = body.orientation.y
                self.ori[i][2] = body.orientation.z

                self.vel[i][0] = body.velocity.x
                self.vel[i][1] = body.velocity.y
                self.vel[i][2] = body.velocity.z
                
                self.acc[i][0] = body.acceleration.x
                self.acc[i][1] = body.acceleration.y
                self.acc[i][2] = body.acceleration.z   
##                self.names[i]=aBody.name
##                self.mass[i]=aBody.mass
##                self.rad[i]=aBody.radius
##                self.pos[i]=aBody.position
##                self.ori[i]=aBody.orientation
##                self.vel[i]=aBody.velocity
##                self.acc[i]=aBody.acceleration

                

        def printBody(self, i):
                print "printing body: ", i
                print "nam :",self.names[i]
                print "mas :",self.mass[i]
                print "rad :",self.rad[i]
                print "pos :",self.pos[i]
                print "vel :",self.vel[i]
                print "acc :",self.acc[i]

        def moveBody(self,source,dest):
                self.names[dest]=self.names[source]
                self.mass[dest]=self.mass[source]
                self.rad[dest]=self.rad[source]
                self.pos[dest]=self.pos[source]
                self.ori[dest]=self.ori[source]
                self.vel[dest]=self.vel[source]
                self.acc[dest]=self.acc[source]
                self.names[source]="OLD"
                
                
        def removeBody(self, i):
                if i != self.player:
                        print "removing body ",i
                        self.printBody(i)
                        if i == self.count -1:
                                print "remove last item"

                        else:
                                self.moveBody(self.count-1, i)
                        self.count -=1
                        self.getPlayerIndex()
                        
                        
        def resetAcc(self):
                for i in range (0, self.count):
                    self.acc[i] = [0.0,0.0,0.0]
                                        
        def addSpace(self):
                #count = len(self.names)-1
                self.allocated +=1
                self.names.append("")
                self.mass.append(0.0)
                self.rad.append(0.0)
                self.pos.append([0.0,0.0,0.0])
                self.ori.append([0.0,0.0,0.0])
                self.vel.append([0.0,0.0,0.0])
                self.acc.append([0.0,0.0,0.0])

