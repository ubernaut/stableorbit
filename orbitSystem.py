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
	def __init__ (self,body_data):
		self.name=body_data[0]
		self.mass=float(body_data[1])
		self.position=Position(body_data[2:5])
		self.velocity=Velocity(body_data[5:8])
                self.acceleration = Acceleration()

##		self.position=Point(body_data[2:5])
##		self.velocity=Point(body_data[5:8])
##		self.acceleration=Point(body_data[5:8])
##		self.acceleration.reset()
	
	def __del__(self):
		del self.position
		del self.velocity
		del self.acceleration
class Point(object):
        def __init(self, position_data):
		self.x=float(position_data[0])
		self.y=float(position_data[1])
		self.z=float(position_data[2])
	def reset(self):
		self.x=0
		self.y=0
		self.z=0
                
class Position(object):
	def __init__ (self,position_data):
		self.x=float(position_data[0])
		self.y=float(position_data[1])
		self.z=float(position_data[2])
class Velocity(object):
	def __init__ (self,velocity_data):
		self.x=float(velocity_data[0])
		self.y=float(velocity_data[1])
		self.z=float(velocity_data[2])
class Acceleration(object):
	def __init__(self):
		self.x=0
		self.y=0
		self.z=0		
	def reset(self):
		self.x=0
		self.y=0
		self.z=0
class System(object):
	def __init__(self, seed, starcount=1, bodycount=2, abodyDistance=3, abodySpeed=0.05):
                random.seed = seed
                self.seed = seed
		self.starCount=starcount
		self.bodyCount= bodycount
		self.bodies=[]
		self.bodyDistance = abodyDistance
		self.bodySpeed = abodySpeed
		self.build()

		print "bodyCount: "+`len(self.bodies)`
		self.stability = 0.5 - self.evaluate(self.bodies)
		self.printed=False
		self.avgStability=0.5 - self.evaluate(self.bodies)
	def build(self):
		bodies=self.bodies
		#N=random.randint(4,self.bodyCount)
                N=self.bodyCount
		for i in range(0,N):
			body_data=[]
			body_data.append("body_" + str(i))
			if i < self.starCount:
				body_data.append(random.uniform(1,10))
				for j in range(0,3):
					body_data.append(random.uniform(-1.5,1.5))
				for j in range(0,3):
					body_data.append(random.uniform(-0.001,0.001))
			else:
				body_data.append(random.uniform(.01,1))
				for j in range(0,3):
					body_data.append(random.uniform(-self.bodyDistance,self.bodyDistance))
				for j in range(0,3):
					body_data.append(random.uniform(-self.bodySpeed,self.bodySpeed))
			body=Body(body_data)
			bodies.append(body)
##	def buildPrime(self):
##		bodies=self.bodies
##		random.seed = self.seed
##                body_data=[]
##                body_data.append("star_" + "0")
##                body_data.append(random.uniform(.8,5))
##                for j in range(0,3):
##                        body_data.append(random.uniform(-.003,.003))
##                for j in range(0,3):
##                        body_data.append(random.uniform(-.001,.001))
##                body=Body(body_data)
##                self.bodies.append(body)
##		planet_n=random.randint(20,40)
##		for i in range(0,planet_n):
##			body_data.append("body_" + str(i))
##			body_data.append(random.uniform(.02,0.5))
##			for j in range(0,3):
##				body_data.append(random.uniform(-20,20))
##			for j in range(0,3):
##				body_data.append(random.uniform(-1,1))
##			abody=Body(body_data)
##			self.bodies.append(abody)
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
	def evaluate(self,bodies):
		kinetic=0.0
		potential=0.0
		G=2.93558*10**-4
		for body in bodies:
			vel = body.velocity
			vel_sq = (vel.x**2 + vel.y**2 + vel.z**2)
			kinetic += 0.5*body.mass*vel_sq
		for i in range(0,len(bodies)):
			current_body=bodies[i]
			current_position=current_body.position
			for j in range(0,i):
				other_body=bodies[j]
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
