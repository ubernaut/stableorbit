#! /usr/bin/python
import dircache
import os
import random
import dircache
import orbitSystem
import Eval
import direct.directbase.DirectStart
import math
from orbitSystem import Body
from orbitSystem import System
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import PointLight,Vec4
from direct.task.Task import Task
#import psyco
#psyco.full()
##class Player(object):
##        def __init__(self):
##                self.position = Point()
                
class Universe(DirectObject):
	def __init__(self, neweval, dt= .02):
                self.zoom = 1
                self.evaluator = neweval
		self.dt=dt
		self.starting=True
		self.mouseX = 0# base.mouseWatcherNode.getMouseX()
                self.mouseY = 0# base.mouseWatcherNode.getMouseY()
#		self.bodies = []#{}
		self.player = Body()
		self.mouseBody = Body()
		self.mouseBody.position.x = 0
		self.mouseBody.position.y = 10
		self.mouseBody.position.z = 0
		self.player.name = "player"
		self.player.mass = .001
		self.player.position.x=0
		self.player.position.x=-15
		self.player.position.x=0
#		self.loadPlayer()
                self.evaluator= neweval
                self.evaluator.system.bodies.append(self.player)
                self.loadPlanets()
#                self.loadPlayer()
#                self.bodies.append(self.player)
		base.camLens.setFar(1000000000000000000000)
                #base.camera.setHpr(0, 0, 0)
		taskMgr.add(self.move,"move")
	def loadPlanets(self):
                for body in self.evaluator.system.bodies:
                        if body.name != "player":
                                body.node = render.attachNewNode(body.name)
                                body.sphere = loader.loadModelCopy("models/planet_sphere")			
                                body.sphere.reparentTo(body.node)
                                body.sphere.setScale((.05 * body.mass) +.1)
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
                        else:
                                self.loadPlayer()
		self.sky = loader.loadModel("models/solar_sky_sphere")
		self.sky_tex = loader.loadTexture("models/stars_1k_tex.jpg")
		self.sky.setTexture(self.sky_tex, 1)
		self.sky.reparentTo(render)
		self.sky.setScale(20000)
	def loadPlayer(self):
                self.player.node = render.attachNewNode("player")
                self.player.model = loader.loadModelCopy("models/fighter")			
                self.player.model.reparentTo(self.player.node)
                self.player.texture = loader.loadTexture("models/texturemap.png")
                self.player.model.setScale(.05)
                self.player.node.setPos(self.player.position.x ,self.player.position.y ,self.player.position.z)
#                self.player.model.reparentTo(render)                
	def move(self,task):
		dt = self.dt
		#base.camera.setPos(0,-22,0)
		#base.camera.printPos()		
		self.evaluator.evaluateStep()
		self.updateMouse()
		if self.starting: 
			dt=dt/2.0
			self.starting=False
		for body in self.evaluator.system.bodies:
##                        if body.name == "player":
##                                print"moving player to"
##                                print body.position.x , body.position.y, body.position.z
			self.move_body(body,dt)
		return Task.cont
	def updateMouse(self):
                if base.mouseWatcherNode.hasMouse():
                        newX = base.mouseWatcherNode.getMouseX()
                        newY = base.mouseWatcherNode.getMouseY()
                        deltaX = self.mouseX - newX
                        deltaY = self.mouseY - newY
                        self.mouseX = newX
                        self.mouseY = newY
                        self.player.orientation.x += (200*deltaX) 
                        self.player.orientation.y -= (200*deltaY)                        
                        dY = self.zoom*math.sin(self.player.orientation.x) 
                        hyp = self.zoom*math.cos(self.player.orientation.x)
                        dZ = hyp * math.sin(self.player.orientation.y) 
                        dX = hyp * math.cos(self.player.orientation.y)
                        base.camera.setHpr(self.player.orientation.x,self.player.orientation.y,0)
##                        base.camera.setPos(self.player.position.x+dX*-1,
##                                           self.player.position.y+dY*-1,
##                                           self.player.position.z+dZ*-1)
                        base.camera.setPos(self.player.position.x,
                                           self.player.position.y+3,
                                           self.player.position.z)                        
                        #base.camera.setHpr(self.player.orientation.x,self.player.orientation.y,0)                        
                        
                #targetBody.orientation.y+=deltaX
                #targetBody.orientation.x+=deltaY
	def move_body(self,body,dt):
		self.set_body_position(body,body.position.x,body.position.y,body.position.z)
	def set_body_position(self,body,x,y,z):
                body.node.setHpr(body.orientation.x, body.orientation.y, body.orientation.z)
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





	

