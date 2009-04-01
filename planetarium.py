#! /usr/bin/python
import dircache
import os
import random
import dircache
import orbitSystem
import Eval
import direct.directbase.DirectStart
from orbitSystem import Body
from orbitSystem import System
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import PointLight,Vec4
from direct.task.Task import Task

class Universe(DirectObject):
	def __init__(self, neweval, dt= .02):
                self.evaluator = neweval
		self.dt=dt
		self.starting=True
		self.bodies = {}
                self.evaluator= neweval
                self.loadPlanets()
		base.camLens.setFar(1000000000000)
		taskMgr.add(self.move,"move")
	def loadPlanets(self):
                for body in self.evaluator.system.bodies:                        
			body.node = render.attachNewNode(body.name)
			body.sphere = loader.loadModelCopy("models/planet_sphere")			
			body.sphere.reparentTo(body.node)
			body.sphere.setScale(body.mass)
			if body.mass < 0.1 :
				body.texture = loader.loadTexture("models/neptune.jpg")
			elif body.mass >= 0.1 and body.mass < .2:
				body.texture = loader.loadTexture("models/pluto.jpg")
			elif body.mass >= .2 and body.mass < .3:
				body.texture = loader.loadTexture("models/venus.jpg")
			elif body.mass >= .3 and body.mass < .4:
				body.texture = loader.loadTexture("models/earthmoon.jpg")
			elif body.mass >= .4 and body.mass < .5:
				body.texture = loader.loadTexture("models/mars.jpg")
			elif body.mass >= .5 and body.mass < .6:
				body.texture = loader.loadTexture("models/pluto.jpg")
			elif body.mass >= .6 and body.mass < .7:
				body.texture = loader.loadTexture("models/saturn.jpg")
			elif body.mass >= .7 and body.mass < .8:
				body.texture = loader.loadTexture("models/jupiter.jpg")
			elif body.mass >= .8 and body.mass < .9:
				body.texture = loader.loadTexture("models/mercury.jpg")
			elif body.mass >= .9 and body.mass < 2:
				body.texture = loader.loadTexture("models/mars.jpg")
			elif body.mass >= 2:
				body.texture = loader.loadTexture("models/sun.jpg")
			else:
				body.texture = loader.loadTexture("models/mars.jpg")
			body.sphere.setTexture(body.texture,1)
			body.node.setPos(body.position.x,body.position.y,body.position.z)
		self.sky = loader.loadModel("models/solar_sky_sphere")
		self.sky_tex = loader.loadTexture("models/stars_1k_tex.jpg")
		self.sky.setTexture(self.sky_tex, 1)
		self.sky.reparentTo(render)
		self.sky.setScale(20000)
	def move(self,task):
		dt = self.dt
		self.evaluator.evaluateStep()
		if self.starting: 
			dt=dt/2.0
			self.starting=False
		for body in self.evaluator.system.bodies:
			self.move_body(body,dt)
		return Task.cont
	def move_body(self,body,dt):
		self.set_body_position(body,body.position.x,body.position.y,body.position.z)
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





	

