#! /usr/local/bin/python
import random
import math
import sys
import os

folder = "system_" + sys.argv[1]


class Body(object):
	def __init__ (self,body_data):
		self.name=body_data[0]
		self.mass=float(body_data[1])
		self.position=Position(body_data[2:5])
		self.velocity=Velocity(body_data[5:8])

		
	
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


class System(object):
	def __init__(self):
		self.bodies=[]
		self.build()
		self.stability = 0.5 - self.evaluate(self.bodies)
		self.printed=False
	
	def build(self):
		bodies=self.bodies
		N=random.randint(2,25)
		for i in range(0,N):
			body_data=[]
			body_data.append("body_" + str(i))
			body_data.append(random.uniform(.01,5))
			for j in range(0,3):
				body_data.append(random.uniform(-15,15))
			for j in range(0,3):
				body_data.append(random.uniform(-0.05,0.05))
			
			body=Body(body_data)
			bodies.append(body)


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
				
				potential -= G*current_body.mass*other_body.mass/radius
		try:	
			return abs(kinetic/potential)
		except:
			return 100.0


class GeneticAlgorithm:
	def __init__(self,populationSize):
		systems=[]
		for i in range(0,populationSize-1):
			systems.append(System())

		systems = self.selection(systems)
		
		
		self.genetitize(populationSize,systems)

            
	def selection(self,systems):

		val_checker=[]
		for system in systems:
			val_checker.append(system.stability)
		val_checker=sorted(val_checker)
		for system in systems:
			if system.stability < val_checker[-1]:
				systems.remove(system)
		for system in systems:
			if system.stability > -0.001 and not system.printed:
				self.write_conditions(system)
				exit()

		return systems
		
	def genetitize(self,populationSize,systems):
		while 1:
			for i in range(len(systems),populationSize):
				systems.append(System())
			self.selection(systems)
			
	def write_conditions(self,system):
		os.chdir("data")
		os.mkdir(folder)
		os.chdir(folder)
		for body in system.bodies:
			pos=body.position
			vel=body.velocity
			data_file = open(body.name,"w+")
			data_file.write(str(body.mass)+"\t"+str(pos.x)+"\t"+str(pos.y)+"\t"+str(pos.z)+"\t"+str(vel.x)+"\t"+str(vel.y)+"\t"+str(vel.z) +"\n")

GeneticAlgorithm(10)
