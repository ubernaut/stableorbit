import direct.directbase.DirectStart
from threading import *
from direct.showbase import DirectObject
from pandac.PandaModules import TextNode, Vec3, Vec4
from pandac.PandaModules import AmbientLight,DirectionalLight
from pandac.PandaModules import PointLight,Spotlight
from pandac.PandaModules import Fog
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from direct.task import *
from direct.actor import Actor
from pandac.PandaModules import TextNode
from pandac.PandaModules import Point2,Point3,Vec3,Vec4
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from random import randint, choice, random
from direct.interval.MetaInterval import Sequence
from direct.interval.FunctionInterval import Wait,Func
import cPickle, sys
import math
import random
#import psyco
#psyco.full()
import sys

bodies={}
accel=[]
test_accel=[]
asteroids=100

def genLabelText(text, i):
  return OnscreenText(text = text, pos = (-1.3, .95-.05*i), fg=(1,1,0,1),
                      align = TextNode.ALeft, scale = .05)

class Universe(DirectObject):
	
	def __init__(self):
		self.destroy=0
		self.title = OnscreenText(text="Planet Simulation with random test particles.",
                              style=1, fg=(1,1,0,1),
                              pos=(0.4,-0.95), scale = .057)
		self.escapeText =   genLabelText("ESC: Quit", 0)
		self.spacekeyText = genLabelText("[Space]: Focus on planetary bodies", 1)
		self.tabkeyText = genLabelText("[Tab]: Focus on test particles", 2)
		
		base.disableMouse()
		base.setBackgroundColor(0,0,0)
		self.starting=True
		alight = AmbientLight('alight')
		alight.setColor(Vec4(0.3, 0.3, 0.3, 1))
		alnp = render.attachNewNode(alight)
		render.setLight(alnp)
	
		self.loadTestParticles()
		self.loadPlanets()
		#self.draw_planet_data(bodies["sun"],0)
		
		self.keys = {"cyclePlanet" : 0, "cycleParticle" :0 }
		
		self.lookAtPlanet=0
		self.lookAtParticle=1
		self.lookAtPlanetCheck=True
		
		self.accept("escape", sys.exit)
		self.accept("space",          self.setKey, ["cyclePlanet", 1])
		self.accept("tab",          self.setKey, ["cycleParticle", 1])
		
		base.camera.reparentTo(bodies["asteroid_1"].node)
		base.camera.lookAt(bodies["sun"].node)
		
		taskMgr.doMethodLater(1, self.draw_planet_data,"draw_data",extraArgs = [])
		taskMgr.add(self.accelerate, "accelerate")
		taskMgr.add(self.move, "move")
		taskMgr.add(self.camera_loop, "move_camera")
		
	def setKey(self, key, val): self.keys[key] = val

	def loadPlanets(self):
		plight=PointLight('plight')
		plight.setColor(Vec4(1, 1, 1, 1))
		for body in bodies.values():
			body.node = render.attachNewNode(body.name)
			body.sphere = loader.loadModelCopy("models/planet_sphere")			
			
			body.sphere.reparentTo(body.node)
			
			if body.mass == 0.0:
				body.sphere.setScale(0.017)
				body.texture = loader.loadTexture("models/armstrong.jpg")
				#body.sphere.setTexture("models/mercury.jpg",1)
			else:
				body.sphere.setScale(.1)
				body.texture = loader.loadTexture(body.texture)
			
			body.sphere.setTexture(body.texture,1)
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
		self.sky.setScale(200)
	
	def loadTestParticles(self):
		for i in range(0,asteroids):
			name = "asteroid_" + str(i)
			mass = 0.0
			pos_x = random.uniform(-3, 3)
			pos_y = random.uniform(-3, 3)
			pos_z = random.uniform(-3, 3)
			vel_x = random.uniform(-.01,.01)
			vel_y = random.uniform(-.01,.01)
			vel_z = random.uniform(-.01,.01)
			body_data=[name,mass,pos_x,pos_y,pos_z,vel_x,vel_y,vel_z]
			body=Body(body_data)
			bodies[body.name]=body
			test_accel.append(body)
			
			

	def accelerate(self,task):
		G=2.93558*10**-4
		for i in range(0,len(accel)):
			current_body=accel[i]
			current_position=current_body.position
			for j in range(0,i):
				if j!=i:
					other_body=accel[j]
					other_position=other_body.position
				
					d_x=(other_position.x-current_position.x)
					d_y=(other_position.y-current_position.y)
					d_z=(other_position.z-current_position.z)
				
					radius = d_x**2 + d_y**2 + d_z**2
					
					grav_mag = G*current_body.mass*other_body.mass/(radius**(3.0/2.0))
					
					grav_x=grav_mag*d_x
					grav_y=grav_mag*d_y
					grav_z=grav_mag*d_z
					
					current_body.acceleration.x += grav_x/current_body.mass
					other_body.acceleration.x -= grav_x/other_body.mass
					
					current_body.acceleration.y += grav_y/current_body.mass
					other_body.acceleration.y -= grav_y/other_body.mass
					
					current_body.acceleration.z += grav_z/current_body.mass
					other_body.acceleration.z -= grav_z/other_body.mass
		
		for i in range(0,len(test_accel)):
			test_body=test_accel[i]
			test_position=test_body.position
			for j in range(0,len(accel)):
				body = accel[j]
				position = body.position
				
				d_x=(position.x-test_position.x)
				d_y=(position.y-test_position.y)
				d_z=(position.z-test_position.z)
				
				radius = d_x**2 + d_y**2 + d_z**2
				
				grav_mag = G*body.mass/(radius**(3.0/2.0))
		
				
				test_body.acceleration.x += grav_mag*d_x
				test_body.acceleration.y += grav_mag*d_y
				test_body.acceleration.z += grav_mag*d_z
				
		return Task.cont
	
	def move(self,task):
		dt = 0.1
		if self.starting: 
			dt=dt/2.0
			self.starting=False

		for body in bodies.values():
			self.move_body(body,dt)

		return Task.cont


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


	def camera_loop(self,task):
		angledegrees = task.time*5
		angleradians = angledegrees * (math.pi / 180.0)
		
		if self.keys["cyclePlanet"]:
			self.lookAtPlanet+=1
			if self.lookAtPlanet==len(accel):
				self.lookAtPlanet=0
			self.keys["cyclePlanet"] = 0
			

		
		if self.keys["cycleParticle"]:
			self.lookAtParticle+=1
			if self.lookAtParticle==len(test_accel):
				self.lookAtParticle=0
			self.keys["cycleParticle"] = 0
			base.camera.reparentTo(test_accel[self.lookAtParticle].node)
			
			
		base.camera.lookAt(accel[self.lookAtPlanet].node)
		
		
		
		#base.camera.setPos(5*math.sin(angleradians),5*math.cos(angleradians),1)
		#base.camera.setPos(5,0,1)
		return Task.cont 

	
	def draw_planet_data(self):
		if self.destroy:
			self.textName.destroy()
			self.textPosition.destroy()
			self.textVelocity.destroy()
		
		
		body = accel[self.lookAtPlanet]
		
		self.textName = OnscreenText(text = body.name, fg=(1,1,0,1), pos = (-1.2, -0.6), scale = 0.07)
		
		position_string= "Position: X =" + str(body.position.x) + ", Y=" + str(body.position.y) + ", Z=" + str(body.position.z)
		self.textPosition = OnscreenText(text = position_string, fg=(1,1,0,1), pos = (-0, -0.6-0.1*1), scale = 0.07)
		
		velocity_string= "Velocity: X =" + str(body.velocity.x) + ", Y=" + str(body.velocity.y) + ", Z=" + str(body.velocity.z)
		self.textVelocity = OnscreenText(text = velocity_string, fg=(1,1,0,1), pos = (-0, -0.6-0.1*2), scale = 0.07)
		#textNodePath.setScale(0.07)
		self.destroy=1
		
		taskMgr.doMethodLater(0.5, self.draw_planet_data,"draw_data",extraArgs = [])

			
		
		
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
	
	def reset(self):
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
	


