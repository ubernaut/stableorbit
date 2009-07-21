import random
import dircache
import random
import math
import sys
import os
import copy
#import psyco
#psyco.full()
#load from xml
class Body(object):
	def __init__ (self,body_data=[]):
                if body_data == []:
                        body_data=["body",1,0,0,0,0,0,0,0,0,0]
		self.name=body_data[0]
		self.mass=float(body_data[1])
		self.position=Point(body_data[2:5])
		self.velocity=Point(body_data[5:8])
		self.acceleration=Point(body_data[5:8])
		self.orientation=Point()
		self.angVelocity=Point()
		self.acceleration.reset()
	
	def __del__(self):
		del self.position
		del self.velocity
		del self.acceleration
       
                
class Point(object):
        def __init__(self, position_data=[0,0,0]):
                self.x=float(position_data[0])
		self.y=float(position_data[1])
		self.z=float(position_data[2])
	def reset(self):
		self.x=0
		self.y=0
		self.z=0
class Star(object):
        def __init__(self, aPos=Point([1,1,1]), aName="default", aPlayer="cos"):
                self.pos = aPos
                self.name = aName
                self.player = aPlayer
            

class System(object):
	def __init__(self, seed, starcount=1, bodycount=2, abodyDistance=3, abodySpeed=0.05):
                random.seed = seed
                self.seed = seed
                self.star = Star()
		self.starCount=starcount
		self.bodyCount= bodycount
		self.bodies=[]
		self.bodyDistance = abodyDistance
		self.bodySpeed = abodySpeed
		self.build()

		print "bodyCount: "+`len(self.bodies)`
		self.stability = 0.5 - self.evaluate()
		self.printed=False
		self.avgStability=0.5 - self.evaluate()
	def getStar(self, body_data):
                body_data.append(random.uniform(1,10))
                for j in range(0,3):
                        body_data.append(random.uniform(-.1,.1))
		for j in range(0,3):
			body_data.append(random.uniform(-0.0,0.0))
		return body_data
	def getPlanet(self, body_data):
#                body_data.append("body_"+len(self.bodies))
                body_data.append(random.uniform(.01,.5))
                for j in range(0,3):
                        body_data.append(random.uniform(-self.bodyDistance,self.bodyDistance))
                for j in range(0,3):
                        body_data.append(random.uniform(-self.bodySpeed,self.bodySpeed))
                return body_data
                
	def build(self):
		bodies=self.bodies
		N=self.bodyCount
		for i in range(0,N):
			body_data=[]
			body_data.append("body_" + str(i))
			if i < self.starCount:
                                body_data = self.getStar(body_data)

			else:
                                body_data = self.getPlanet(body_data)

			body=Body(body_data)
			bodies.append(body)
	def addSinglePlanet(self):
                print "adding Body"
                body_data = []
                body_data.append("body_X")
                body_data = self.getPlanet(body_data)
                aBody = Body(body_data)
                otherBodies = []
                otherBodies.append(self.bodies[0])
                otherBodies.append(aBody)
                while self.evaluateBodies(otherBodies)>1:
                        body_data = []
                        body_data.append("body_X")
                        body_data = self.getPlanet(body_data)
                        aBody = Body(body_data)
                        otherBodies = []
                        otherBodies.append(self.bodies[0])
                        otherBodies.append(aBody)
                self.bodies.append(aBody)
                

                
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
			self.bodies[whichBody].position.x+= alphaPosition * (random.uniform(-.000001,.000001))
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

        
class GridSystem(object):
        def __init__(self, bodies=[]):
                self.count = bodies.length()
                N = self.count
                self.names[N] = "un-named"
                self.mass[N] = 0.0
                self.pos[N][3] = 0.0
                self.vel[N][3] = 0.0
                self.acc[N][3] = 0.0

                i = 0;
                for body in bodies:
                        self.names[i] = body.name
                        self.mass[i] = body.mass

                        self.pos[i][0] = body.position.x
                        self.pos[i][1] = body.position.y
                        self.pos[i][2] = body.position.z
                       
                        self.vel[i][0] = body.velocity.x
                        self.vel[i][1] = body.velocity.y
                        self.vel[i][2] = body.velocity.z

                        self.acc[i][0] = body.acceleration.x
                        self.acc[i][1] = body.acceleration.y
                        self.acc[i][2] = body.acceleration.z
                        i+=1
