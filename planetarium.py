#! /usr/bin/python
import dircache
import os
import random
import dircache
import orbitSystem
import Eval
import math
from orbitSystem import Body
from orbitSystem import System
from pandac.PandaModules import loadPrcFileData
def config():
        loadPrcFileData("", "window-title stableorbit")
        print "Enter 'f' 'Enter' for fullscreen or just 'Enter' for windowed"
        fullVar = raw_input()
        if(fullVar=="f"):        
                loadPrcFileData("", "fullscreen 1")
        print "Enter '1' for 1200x600"
        print "      '2' for 1440x900"
        print "      '3' for 1600x1050"
        print "or 'Enter' for default 800x600"
        screenVar = raw_input()
        if screenVar == "1":
                loadPrcFileData("", "win-size 1200 600")
        if screenVar == "2":
                loadPrcFileData("", "win-size 1440 900")
        if screenVar == "3":
                loadPrcFileData("", "win-size 1600 1050")
        loadPrcFileData("","x-wheel-left-button 6")
        loadPrcFileData("","x-wheel-right-button 7")
config()

from direct.showbase import DirectObject
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import PointLight,Vec4
from direct.task.Task import Task
import direct.directbase.DirectStart


class Universe(DirectObject):
	def __init__(self, neweval, dt=.002, starList=[]):
                #messenger.toggleVerbose()
                self.stars=starList
                self.mouselook=True
                self.zoom = 4
                self.mapMode = False
                self.evaluator = neweval
                self.hudScale = 1
                self.objectScale=.01
                self.starScale = 10
                self.skyScale=200000
		self.dt=dt
		self.starting=True
		self.mouseX = 0
                self.mouseY = 0
                self.dX=0
                self.dY=0
                self.dZ=0
                self.player = Body()
		self.mouseBody = Body()
		self.mouseBody.name = "mouse"
		self.player.name = "player"
		self.player.mass = .000000001
		self.player.position.x=0
		self.player.position.y=1
		self.player.position.z=0
		self.player.bodies=[]
                self.evaluator= neweval
                self.evaluator.system.bodies.append(self.player)
                self.evaluator.system.moveToStar()
                self.loadPlanets()
                if len(starList)>0:
                        self.loadStars()
		base.camLens.setFar(170000000000000000000000000000000000000)
		taskMgr.add(self.move,"move")
		
        
        def loadStars(self):
                print "loading stars"
                for star in self.stars:
                        star.body.node = render.attachNewNode(star.body.name)
                        star.body.sphere = loader.loadModelCopy("models/dodecahedron")			
                        star.body.sphere.reparentTo(star.body.node)
                        star.body.sphere.setScale(self.starScale)
                        star.body.node.setPos(star.body.position.x,star.body.position.y,star.body.position.z)
        
	def loadPlanets(self):
                for body in self.evaluator.system.bodies:
                        if body.name != "player":
                                #if body.name == "sol":
                                body.node = render.attachNewNode(body.name)
                                body.sphere = loader.loadModelCopy("models/planet_sphere")			
                                body.sphere.reparentTo(body.node)
                                #body.sphere.setScale((.05 * body.mass) +.005)
                                #body.sphere.setScale(1)
                                body.sphere.setScale((body.mass/1000)+self.objectScale)
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
                                print "yo"
                                #self.sky = loader.loadModelCopy("models/planet_sphere")
                                self.sky = loader.loadModel("models/solar_sky_sphere")
#                                self.sky_tex = loader.loadTexture("models/stars_1k_tex.jpg")
                                self.sky_tex = loader.loadTexture("models/startex.jpg")
                                self.sky.setTexture(self.sky_tex, 1)
                                self.sky.setScale(self.skyScale)
                                self.loadPlayer(body)
                                self.sky.reparentTo(render)
        def scaleUp(self):
                self.starScale*= 1.01
                print self.starScale
                for star in self.stars:
                        star.body.sphere.setScale(self.starScale)
                        
        def scaleDown(self):
                self.starScale*= .99
                print self.starScale
                for star in self.stars:
                        star.body.sphere.setScale(self.starScale)
                                                
		
	def loadRoid(self, abody):
                if(len(self.player.bodies)<10):
                        self.player.bodies.append(abody)
                        self.evaluator.system.bodies.append(abody)
                        abody.node = render.attachNewNode(abody.name)
                        abody.model = loader.loadModelCopy("models/planet_sphere")			
                        abody.model.reparentTo(abody.node)
                        abody.texture = loader.loadTexture("models/pluto.jpg")
                        abody.model.setScale(.01)
                        abody.node.setPos(abody.position.x ,abody.position.y ,abody.position.z)
                return
        
        def deloadRoid(self):
                if(len(self.player.bodies) >0):
                        abody = self.player.bodies.pop()
                        self.evaluator.system.bodies.pop()
                        abody.node.detachNode()
                return
#                abody.node = render.attachNewNode(abody.name)
#                abody.model = loader.loadModelCopy("models/planet_sphere")			
#                abody.model.reparentTo(abody.node)
#                abody.texture = loader.loadTexture("models/pluto.jpg")
#                abody.model.setScale(.01)
#                abody.node.setPos(abody.position.x ,abody.position.y ,abody.posit
	def loadPlayer(self, abody):
                abody.node = render.attachNewNode(abody.name)
                abody.model = loader.loadModelCopy("models/fighter")			
                abody.model.reparentTo(abody.node)
                if abody.name == "player":
                        abody.texture = loader.loadTexture("models/texturemap.png")
                elif abody.name == "mouse":
                        abody.texture = loader.loadTexture("models/sun.jpg")
                abody.model.setScale(.003)
                abody.node.setPos(abody.position.x ,abody.position.y ,abody.position.z)
        def exit(self):
                quit()
                return
        def fullscreen(self):
                print "doh"

##                if(self.DirectObject.ConfigVariableManager.fullscreen==0):
##                        self.DirectObject.ConfigVariableManager.fullscreen=1
##                else:
##                        self.DirectObject.ConfigVariableManager.fullscreen=0
                                  
	def move(self,task):
                self.accept("mouse6", self.tiltLeft)
                self.accept("mouse7", self.tiltRight)
                self.accept("mouse5", self.tiltLeft)
                self.accept("mouse4", self.tiltRight)
                self.accept("mouse8", self.tiltLeft)
                self.accept("mouse9", self.tiltRight)
                self.accept("x_wheel_left", self.tiltLeft)
                self.accept("x_wheel_right", self.tiltRight)
                self.accept("w", self.tiltLeft)
                self.accept("r", self.tiltRight)
                self.accept("mouse2", self.handlemouse2Click)
                self.accept("mouse3", self.handleRightMouseClick)
                self.accept("mouse1", self.handleLeftMouseClick)
		self.accept("wheel_up", self.zoomIn)
		self.accept("wheel_down", self.zoomOut)
		self.accept("escape", self.exit)
		self.accept("space",self.stop)
		self.accept("d",self.brake)
		self.accept("e",self.accelerate)
		self.accept("f",self.fullscreen)
		self.accept("m",self.togglemap)
		self.accept("[",self.scaleDown)
		self.accept("]",self.scaleUp)
		self.accept("l",self.togglemouselook)
		#self.accept("")
		dt = self.dt
		if not self.mapMode:
                        self.evaluator.evaluateStep()
		self.updateMouse(self.player)
		if self.starting: 
			dt=dt/2.0
			self.starting=False
		for body in self.evaluator.system.bodies:
			self.move_body(body,dt)
		return Task.cont
	def tiltLeft(self):
                print "left"
                self.player.orientation.z-=10
        def tiltRight(self):
                print "right"
                self.player.orientation.z+=10
	def togglemouselook(self):
                print "toggling mouselook"
                if self.mouselook:
                        self.mouselook = False
                else:
                        self.mouselook = True
	def togglemap(self):
                print "toggling map"
                if (self.mapMode):
                        self.mapMode=False
                        self.zoom=1.1
                        #base.disableMouse()
                else:
                        self.mapMode=True
                        self.zoom = 59000
                        #base.enableMouse()
                                  
	def accelerate(self):                                  
                print "accelerating ship"
                self.player.acceleration.x+=self.dX/50
                self.player.acceleration.y+=self.dY/50
                self.player.acceleration.z+=self.dZ/50                                  
                return
        def stop(self):
                print "stopping ship"
                self.player.velocity.x=0
                self.player.velocity.y=0
                self.player.velocity.z=0
                return
        def brake(self):
                print "slowing ship"
                self.player.acceleration.x-=self.dX/50
                self.player.acceleration.y-=self.dY/50
                self.player.acceleration.z-=self.dZ/50 
	def handleMouse2(self):
                print "deccelerating ship"
                self.player.acceleration.x-=self.dX/10
                self.player.acceleration.y-=self.dY/10
                self.player.acceleration.z-=self.dZ/10
        def handlemouse2Click(self):
                print "mouse2"
                self.togglemouselook()
        def handlemouseLeftClick(self):
                print "mouseLeft"
        def handlemouseRightClick(self):
                print "mouseRight"
        def handleLeftMouseClick(self):
                print "impactor deployed"
                abody=Body()
                abody.velocity.x = self.player.velocity.x
                abody.velocity.y = self.player.velocity.y
                abody.velocity.z = self.player.velocity.z
                abody.position.x = self.player.position.x
                abody.position.y = self.player.position.y
                abody.position.z = self.player.position.z
                abody.acceleration.x += self.dX/15
                abody.acceleration.y += self.dY/15
                abody.acceleration.z += self.dZ/15
                abody.mass =0.00000001
                self.loadRoid(abody)                                  
                return
        def handleRightMouseClick(self):
                print "removing impactor"
                self.deloadRoid()

                
	def zoomIn(self):
                self.zoom*=0.9
                print self.zoom
                #self.scaleDown()
                return
        def zoomOut(self):
                self.zoom*=1.1
                print self.zoom
                #self.scaleUp()
                if self.zoom > 60000:
                        self.zoomIn()
                return
	def updateMouse(self, abody):
                if (base.mouseWatcherNode.hasMouse() and self.mouselook):
                        newX = base.mouseWatcherNode.getMouseX()
                        newY = base.mouseWatcherNode.getMouseY()                        
                        deltaX = self.mouseX - newX
                        deltaY = self.mouseY - newY
                        self.mouseX = newX
                        self.mouseY = newY
                        if abody.orientation.y >360:
                                abody.orientation.y -=360
                        if abody.orientation.x >360:
                                abody.orientation.x -=360
                        if abody.orientation.y > 180:
                                abody.orientation.y += (360*deltaY)
                        else:
                                abody.orientation.y -= (360*deltaY)
                                
                        if abody.orientation.y > 180:
                                abody.orientation.x -= (360*deltaX)
                        else:
                                abody.orientation.x += (360*deltaX)
                        
                        self.dZ = self.zoom*math.sin((-abody.orientation.y+180)*(math.pi / 180.0)) 
                        hyp = self.zoom*math.cos((-abody.orientation.y+180)*(math.pi / 180.0))
                        self.dX = hyp * math.sin((-abody.orientation.x+180)*(math.pi / 180.0)) 
                        self.dY = hyp * math.cos((-abody.orientation.x+180)*(math.pi / 180.0))
                base.camera.setHpr(abody.orientation.x,
                                   abody.orientation.y,abody.orientation.z)
                base.camera.setPos(abody.position.x-self.dX,
                                   abody.position.y-self.dY,
                                   abody.position.z-self.dZ)              

	def move_body(self,body,dt):
		self.set_body_position(body,body.position.x,body.position.y,body.position.z)
	def set_body_position(self,body,x,y,z):
                body.node.setPos(x,y,z) 
                body.node.setHpr(body.orientation.x, body.orientation.y, body.orientation.z)
		               
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
