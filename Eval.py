import orbitSystem
import random
import dircache
import random
import math
import sys
import os
import copy
#import psyco
#psyco.full()

#add collision detection
class Eval:
	def __init__(self,aSystem, maxMark=10000, dt = .2):
		self.dt=dt
		self.system = aSystem
		self.maxMark=maxMark
		self.fitness=self.system.evaluate(self.system.bodies)
		self.sumFit=self.system.evaluate(self.system.bodies)
		self.t=0
		self.count=1
		
	def evaluateStep(self):
                self.accelerate()
                for body in self.system.bodies:
                        self.calculate_velocity(body,self.dt)
                        self.calculate_position(body,self.dt)
                        body.acceleration.reset()
			self.sumFit+=self.system.evaluate(self.system.bodies)
			self.t+=self.dt
		self.count+=1	

	def evaluate(self):
		self.t=0
		self.count=1
		self.accelerate()
		self.sumFit=0
		while self.count<self.maxMark:
                        self.evaluateStep()			
		self.fitness = self.system.evaluate(self.system.bodies)
		self.avgStability = self.sumFit/self.count
		return self.avgStability
	def accelerate(self):		
		G=2.93558*10**-4
		epsilon = 0.01
		for i in range(0,len(self.system.bodies)):
			current_body=self.system.bodies[i]
			current_position=current_body.position
			for j in range(0,i):
				other_body=self.system.bodies[j]
				other_position=other_body.position
				d_x=(other_position.x-current_position.x)
				d_y=(other_position.y-current_position.y)
				d_z=(other_position.z-current_position.z)
				radius = d_x**2 + d_y**2 + d_z**2
				grav_mag=0
				
				if radius >0:
					grav_mag = G/((radius+epsilon)**(3.0/2.0))
				else:
                                        radius = 0.001
                                        grav_mag = G/((radius+epsilon)**(3.0/2.0))
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
