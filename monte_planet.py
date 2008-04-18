#! /usr/bin/python

import dircache

import os

#import psyco

import random

import dircache

#psyco.full()

import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import PointLight,Vec4
from direct.task.Task import Task

bodies={}

        
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
		del self.acceleration
		

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


class Universe(DirectObject):
	def __init__(self,dt=0.1):
		self.loadPlanets()
		self.dt=dt
		self.starting=True
		taskMgr.add(self.accelerate,"accelerate")
		taskMgr.add(self.move,"move")
	
	def loadPlanets(self):
		for body in bodies.values():
			body.node = render.attachNewNode(body.name)
			body.sphere = loader.loadModelCopy("models/planet_sphere")			
			
			body.sphere.reparentTo(body.node)
			
			body.sphere.setScale(0.5)
			body.texture = loader.loadTexture("models/neptune.jpg")

			body.sphere.setTexture(body.texture,1)
			body.node.setPos(body.position.x,body.position.y,body.position.z)
		

		
		self.sky = loader.loadModel("models/solar_sky_sphere")
		self.sky_tex = loader.loadTexture("models/stars_1k_tex.jpg")
		self.sky.setTexture(self.sky_tex, 1)
		self.sky.reparentTo(render)
		self.sky.setScale(200)

	def move(self,task):
		dt = self.dt
		if self.starting: 
			dt=dt/2.0
			self.starting=False

		for body in bodies.values():
			self.move_body(body,dt)

		return Task.cont
			
	def accelerate(self,task):
		accel=bodies.values()
		G=2.93558*10**-4
		for i in range(0,len(accel)):
			current_body=accel[i]
			current_position=current_body.position
			for j in range(0,i):
				other_body=accel[j]
				other_position=other_body.position
			
				d_x=(other_position.x-current_position.x)
				d_y=(other_position.y-current_position.y)
				d_z=(other_position.z-current_position.z)
			
				radius = d_x**2 + d_y**2 + d_z**2
				
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

			
	def move_body(self,body,dt):
		self.calculate_velocity(body,dt)
		body.acceleration.reset()
		self.calculate_position(body,dt)
		self.set_body_position(body,body.position.x,body.position.y,body.position.z)

	def calculate_velocity(self,body,dt):
		body.velocity.x += dt*body.acceleration.x
		body.velocity.y += dt*body.acceleration.y
		body.velocity.z += dt*body.acceleration.z

	def calculate_position(self,body,dt):
		body.position.x += dt*body.velocity.x
		body.position.y += dt*body.velocity.y
		body.position.z += dt*body.velocity.z

	def set_body_position(self,body,x,y,z):
		body.node.setPos(x,y,z)




	

def set_conditions(data_folder):
	a=dircache.listdir(data_folder)
	try:
		a.remove('.svn')
		a.remove('evolotion')
	except:
		print "svn wasnt there"
	body_data=[]
	for f in a:
		values = open(data_folder+f).readlines()
		v = values[0]
		body_data = v.split()
		body_data.insert(0,f)
		body=Body(body_data)
		bodies[body.name]=body

	
set_conditions('data/system_4/')	
U=Universe()			
run()





	

