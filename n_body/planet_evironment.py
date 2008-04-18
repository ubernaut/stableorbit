import direct.directbase.DirectStart
from threading import *
from direct.showbase import DirectObject
from pandac.PandaModules import TextNode, Vec3, Vec4
from pandac.PandaModules import AmbientLight,DirectionalLight
from pandac.PandaModules import PointLight,Spotlight
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from direct.task import Task
from direct.actor import Actor 
import math
import psyco
psyco.full()
import sys

bodies={}
accel=[]

class Universe(DirectObject):
	
	def __init__(self):
		base.disableMouse()
		base.setBackgroundColor(0,0,0)
		self.starting=True
		alight = AmbientLight('alight')
		alight.setColor(Vec4(0.01, 0.01, 0.01, 1))
		alnp = render.attachNewNode(alight)
		render.setLight(alnp)

		self.loadPlanets()

		taskMgr.add(self.accelerate, "accelerate")
		taskMgr.add(self.move, "move")
		taskMgr.add(self.move_camera, "move_camera")

	def loadPlanets(self):
		plight=PointLight('plight')
		plight.setColor(Vec4(1, 1, 1, 1))
		for body in bodies.values():
			body.node = render.attachNewNode(body.name)
			body.sphere = loader.loadModelCopy("models/planet_sphere")			
			body.texture = loader.loadTexture(body.texture)
			body.sphere.reparentTo(body.node)
			body.sphere.setTexture(body.texture,1)
			body.sphere.setScale(body.radius/bodies["sun"].radius*2)
			body.node.setPos(body.position.x,body.position.y,body.position.z)
		
		plnp = render.attachNewNode(plight)
		plnp.reparentTo(bodies["sun"].node)		
		render.setLight(plnp)

		alight = AmbientLight('alight')
		alight.setColor(Vec4(1, 1, 1, 1))
		alnp = render.attachNewNode(alight)
		bodies["sun"].node.setLight(alnp)


		self.sky = loader.loadModel("models/solar_sky_sphere")
		self.sky_tex = loader.loadTexture("models/stars_1k_tex.jpg")
		self.sky.setTexture(self.sky_tex, 1)
		self.sky.reparentTo(render)
		self.sky.setScale(500)

	def accelerate(self,task):
		G=2.93558*10**-4
		for i in range(0,len(accel)):
			current_body=accel[i]
			current_position=current_body.position
			for j in range(0,i):
				if j!=i:
					other_body=accel[j]
					other_position=other_body.position
				
					self.d_x=(other_position.x-current_position.x)
					self.d_y=(other_position.y-current_position.y)
					self.d_z=(other_position.z-current_position.z)
				
					radius = self.d_x**2 + self.d_y**2 + self.d_z**2
					
					grav_mag = G*current_body.mass*other_body.mass/(radius**(3.0/2.0))
					
					grav_x=grav_mag*self.d_x
					grav_y=grav_mag*self.d_y
					grav_z=grav_mag*self.d_z
					
					current_body.acceleration.x += grav_x/current_body.mass
					other_body.acceleration.x -= grav_x/other_body.mass
					
					current_body.acceleration.y += grav_y/current_body.mass
					other_body.acceleration.y -= grav_y/other_body.mass
					
					current_body.acceleration.z += grav_z/current_body.mass
					other_body.acceleration.z -= grav_z/other_body.mass
		return Task.cont
	
	def move(self,task):
		dt = 0.1

		if self.starting: 
			dt=dt/2.0
			self.starting=False

		for body in bodies.values():
			body.velocity.x += dt*body.acceleration.x
			body.velocity.y += dt*body.acceleration.y
			body.velocity.z += dt*body.acceleration.z

			body.acceleration.x = 0
			body.acceleration.y = 0
			body.acceleration.z = 0

			body.position.x += dt*body.velocity.x
			body.position.y += dt*body.velocity.y
			body.position.z += dt*body.velocity.z
			

			body.node.setPos(body.position.x*10,body.position.y*10,body.position.z*10)

		return Task.cont
	
	def move_camera(self,task):

		angledegrees = task.time*10
		angleradians = angledegrees * (math.pi / 180.0)
		base.camera.reparentTo(bodies["earthmoon"].node)
		base.camera.setPos(1.5*math.cos(angleradians),1.5*math.sin(angleradians),0.1)
		#base.camera.reparentTo(bodies["earthmoon"].node)
		base.camera.lookAt(bodies["earthmoon"].node)
		return Task.cont 

class Body(object):
	def __init__ (self,body_data):
		self.name=body_data[0]
		self.node=""
		self.sphere=""
		self.radius=float(body_data[-1])
		self.texture= "models/" + self.name + ".jpg"
		self.mass=float(body_data[1])
		self.position=Position(body_data[2:5])
		self.velocity=Velocity(body_data[5:8])
		self.acceleration=Acceleration()

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
		



def set_conditions():
	file = open('./initial_conditions/conditions.txt').readlines()
	for line in file:
		body_data = line.split()
		body=Body(body_data)
		bodies[body.name]=body
		accel.append(body)

set_conditions()

U=Universe()

run()
	


