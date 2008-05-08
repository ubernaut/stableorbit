#! /usr/local/bin/python
import random
import math
import sys
import os
import copy
import psyco
psyco.full()

class Body(object):
	def __init__ (self,body_data):
		self.name=body_data[0]
		self.mass=float(body_data[1])
		self.position=Position(body_data[2:5])
		self.velocity=Velocity(body_data[5:8])
		self.acceleration=Acceleration()
	def __del__(self):
		del self.position
		del self.velocity

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

	def __init__(self):
		self.starCount=random.randint(1,3)
		self.bodies=[]		
		self.printed=False

		self.starAlphaMass = 2
		self.starAlphaPosition = 0.01
		self.starAlphaVelocity = 0.01

		self.planetAlphaMass = .1
		self.planetAlphaPosition = 50
		self.planetAlphaVelocity = 2
	      
		self.build()
		self.stability = self.evaluate(self.bodies)
		self.avgStability=self.evaluate(self.bodies)
		


	def build(self):
		bodies=self.bodies
		N=random.randint(2,10)
		for i in range(0,N):
			body_data=[]
			body_data.append("body_" + str(i))
			if i <= self.starCount:
				body_data.append(random.uniform(1,10*self.starAlphaMass))
				for j in range(0,3):
					body_data.append(random.uniform(-self.starAlphaPosition,self.starAlphaPosition))
				for j in range(0,3):
					body_data.append(random.uniform(-self.starAlphaVelocity,self.starAlphaVelocity))
			else:
				body_data.append(random.uniform(self.planetAlphaMass,10*self.planetAlphaMass))
				for j in range(0,3):
					body_data.append(random.uniform(-self.planetAlphaPosition,self.planetAlphaPosition))
				for j in range(0,3):
					body_data.append(random.uniform(-self.planetAlphaVelocity,self.planetAlphaVelocity))
			body=Body(body_data)
			bodies.append(body)
					
	def mutate(self, alphaMass, alphaPosition, alphaVelocity):
		

		whichBody=random.randint(0,len(self.bodies)-1)
		
		oldPosition =copy.deepcopy(self.bodies[whichBody].position)
		oldVelocity =copy.deepcopy(self.bodies[whichBody].velocity)
		
		if whichBody <= self.starCount:
			
			self.bodies[whichBody].position.x+= alphaPosition * (random.uniform(-self.starAlphaPosition,self.starAlphaPosition))
			self.bodies[whichBody].velocity.x+= alphaVelocity * (random.uniform(-self.starAlphaVelocity,self.starAlphaVelocity))
			self.bodies[whichBody].position.y+= alphaPosition * (random.uniform(-self.starAlphaPosition,self.starAlphaPosition))
			self.bodies[whichBody].velocity.y+= alphaVelocity * (random.uniform(-self.starAlphaVelocity,self.starAlphaVelocity))
			self.bodies[whichBody].position.z+= alphaPosition * (random.uniform(-self.starAlphaPosition,self.starAlphaPosition))
			self.bodies[whichBody].velocity.z+= alphaVelocity * (random.uniform(-self.starAlphaVelocity,self.starAlphaVelocity))
			self.bodies[whichBody].mass += alphaMass * random.uniform(-self.bodies[whichBody].mass,10*self.starAlphaMass)
			
			#print `abs(self.bodies[whichBody].position.z)+abs(self.bodies[whichBody].position.x)+abs(self.bodies[whichBody].position.y)`
			if abs(self.bodies[whichBody].position.z)+abs(self.bodies[whichBody].position.x)+abs(self.bodies[whichBody].position.y)>self.starAlphaPosition:
				self.bodies[whichBody].position.x=self.starAlphaPosition
				self.bodies[whichBody].position.y=self.starAlphaPosition
				self.bodies[whichBody].position.z=self.starAlphaPosition
			if abs(self.bodies[whichBody].velocity.z)+abs(self.bodies[whichBody].velocity.x)+abs(self.bodies[whichBody].velocity.y)>self.starAlphaVelocity:
				self.bodies[whichBody].velocity.x=self.starAlphaVelocity
				self.bodies[whichBody].velocity.y=self.starAlphaVelocity
				self.bodies[whichBody].velocity.z=self.starAlphaVelocity
			if self.bodies[whichBody].mass >=10*self.starAlphaMass:
				self.bodies[whichBody].mass=10*self.starAlphaMass - .1
			if self.bodies[whichBody].mass <= 0:
				self.bodies[whichBody].mass=0.1
				print "negetive mass"

		else:
			self.bodies[whichBody].position.x+= alphaPosition * (random.uniform(-self.planetAlphaPosition,self.planetAlphaPosition))
			self.bodies[whichBody].velocity.x+= alphaVelocity * (random.uniform(-self.planetAlphaVelocity,self.planetAlphaVelocity))
			self.bodies[whichBody].position.y+= alphaPosition * (random.uniform(-self.planetAlphaPosition,self.planetAlphaPosition))
			self.bodies[whichBody].velocity.y+= alphaVelocity * (random.uniform(-self.planetAlphaVelocity,self.planetAlphaVelocity))
			self.bodies[whichBody].position.z+= alphaPosition * (random.uniform(-self.planetAlphaPosition,self.planetAlphaPosition))
			self.bodies[whichBody].velocity.z+= alphaVelocity * (random.uniform(-self.planetAlphaVelocity,self.planetAlphaVelocity))
			self.bodies[whichBody].mass += alphaMass * random.uniform(-self.bodies[whichBody].mass,self.planetAlphaMass)
			if abs(self.bodies[whichBody].position.z)+abs(self.bodies[whichBody].position.x)+abs(self.bodies[whichBody].position.y)>self.planetAlphaPosition:
				self.bodies[whichBody].position=oldPosition
			if abs(self.bodies[whichBody].velocity.z)+abs(self.bodies[whichBody].velocity.x)+abs(self.bodies[whichBody].velocity.y)<self.planetAlphaVelocity:
				self.bodies[whichBody].velocity=oldVelocity
			
			if self.bodies[whichBody].mass <= 0:
				self.bodies[whichBody].mass=0.1
				print "negetive mass"
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
			return "divbyzero"
class Eval:
	def __init__(self,aSystem, maxMark):
		self.dt=.02
		self.system = aSystem
		self.maxMark=maxMark
		self.fitness=self.system.evaluate(self.system.bodies)
		self.sumFit=self.system.evaluate(self.system.bodies)
		self.avgStability= self.fitness
		self.evaluate
	def evaluate(self):
		t=0
		count=1
		self.accelerate(self.system)
		self.calculate_velocity(body,self.dt/2.0)
		self.calculate_position(body,self.dt)
		self.sumFit=0
		totalCount = 0
		for count in range (0,self.maxMark):
			self.accelerate(self.system)
			for body in self.system.bodies:
				self.calculate_velocity(body,self.dt)
				self.calculate_position(body,self.dt)
				body.acceleration.reset()
			self.sumFit+=self.system.evaluate(self.system.bodies)
			
			t+=self.dt
			count+=1
			totalCount = count
			
		self.fitness = self.system.evaluate(self.system.bodies)
		self.avgStability = self.sumFit/totalCount
		
		return self.avgStability		

	
	def accelerate(self,system):
		bodies = system.bodies
		G=2.93558*10**-4
		for i in range(0,len(bodies)):
			current_body=bodies[i]
			current_position=current_body.position
			for j in range(0,i):
				other_body=bodies[j]
				other_position=other_body.position
				d_x=(other_position.x-current_position.x)
				d_y=(other_position.y-current_position.y)
				d_z=(other_position.z-current_position.z)
				radius = d_x**2 + d_y**2 + d_z**2
				grav_mag=0
				if radius >0:
					grav_mag = G/(radius**(3.0/2.0))
				grav_x=grav_mag*d_x
				grav_y=grav_mag*d_y
				grav_z=grav_mag*d_z
				
				current_body.acceleration.x += grav_x*other_body.mass
				other_body.acceleration.x -= grav_x*current_body.mass
				
				current_body.acceleration.y += grav_y*other_body.mass
				other_body.acceleration.y -= grav_y*current_body.mass
				
				current_body.acceleration.z += grav_z*other_body.mass
				other_body.acceleration.z -= grav_z*current_body.mass

	def calculate_velocity(self,body,dt):
		body.velocity.x += dt*body.acceleration.x
		body.velocity.y += dt*body.acceleration.y
		body.velocity.z += dt*body.acceleration.z

	def calculate_position(self,body,dt):
		body.position.x += dt*body.velocity.x
		body.position.y += dt*body.velocity.y
		body.position.z += dt*body.velocity.z

class GeneticAlgorithm:
	def __init__(self,popSize):
		self.population =[]
		self.nextGen = []
		self.maxMark = 100000;
		self.popSize = popSize
		self.alphaRate= .1
		self.currMark=1
		self.avgFitness=0
		self.sumFitness=0		
		aSystem=System()
		self.goalFitness = 0.5
		self.goalMax = 0.7
		self.goalMin = 0.1
		while len(self.population)<popSize:
			aSystem=System()
			clientProc = Eval(aSystem,1)
			print"adding:"
			print`len(self.population)`
			print"clientProc.fitness"
			print`clientProc.fitness`
			self.population.append(aSystem)
		self.markN()
	def markN(self):
		print "get N systems which pass the initial viral thm"
		for mark in range (1,self.maxMark):
			print "compute viral fitness for "+`mark`+" dt iterations"
			sysVar =0
			sumFitness = 0
			self.nextGen = []
			for i in range(0,self.popSize):
				aSystem = self.population.pop()
				folder ="mark-"+`mark`+"sys-"+`sysVar`
				backUpSys = copy.deepcopy(aSystem)
				clientProc = Eval(aSystem,mark)
				sysVar+=1
				if clientProc.avgStability < self.goalMax and clientProc.avgStability > self.goalMin  :
					self.nextGen.append(copy.deepcopy(aSystem))
					#print "adding:"
					#print len(self.nextGen)
					if mark%1000 == 0:
						print"clientProc.fitness"
						print`clientProc.fitness`
						print 'clientProc.avgStability'
						print`clientProc.avgStability`
						self.write_conditions(aSystem,folder+"dt")
						self.write_conditions(backUpSys, folder)
				else:
					if clientProc.fitness == "divbyzero":
						aSystem = System()
						self.nextGen.append(copy.deepcopy(aSystem))
						print "div by zero error, building a new system"
					else:
						aSystem.mutate(.1,.1,.1)
						self.nextGen.append(copy.deepcopy(aSystem))
			self.population = copy.deepcopy(self.nextGen)
	def write_conditions(self,system,folder):
		os.chdir("data")
		os.mkdir(folder)
		os.chdir(folder)
		print"recording a mark:"+folder
		
		for body in system.bodies:
			pos=body.position
			vel=body.velocity
			data_file = open(body.name,"w+")
			data_file.write(str(body.mass)+"\t"+str(pos.x)+"\t"+str(pos.y)+"\t"+str(pos.z)+"\t"+str(vel.x)+"\t"+str(vel.y)+"\t"+str(vel.z) +"\n")
		os.chdir("..")
		os.chdir("..")
		
GeneticAlgorithm(10)

