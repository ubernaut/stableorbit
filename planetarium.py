#! /usr/bin/python
import dircache
import os
import random
import dircache
import orbitSystem
import soPhysics
import math
from orbitSystem import Body
from orbitSystem import System
import interactiveConsole
from pandac.PandaModules import loadPrcFileData
from pandac.PandaModules import *
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
        else:
                loadPrcFileData("", "win-size 1200 600")


from direct.showbase import DirectObject
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import PointLight,Vec4
from direct.task.Task import Task
import direct.directbase.DirectStart

#import interactiveConsole

class Universe(DirectObject):
	def __init__(self, neweval, starList=[], console=[]):
                #messenger.toggleVerbose()
                self.stars=starList
                self.mouselook=True
                self.zoom = .33
                self.mapMode = False
                self.evaluator = neweval
                self.hudScale = 1
                self.objectScale=.01
                self.starScale = 10
                self.skyScale=50000
		self.dt=.02
		self.starting=True
		self.mouseX = 0
                self.mouseY = 0
                self.dX=0
                self.dY=0
                self.dZ=0
                self.player = Body()
##		self.mouseBody = Body()
##		self.mouseBody.name = "mouse"
		self.player.name = "player"
		self.player.mass = 0
		self.player.position.x=0
		self.player.position.y=0
		self.player.position.z=-0.04
		self.player.orientation.y=90
		self.accRate =2
#		self.player.bodies=[]
#		self.evaluator.system.bodies.append(self.player)
		neweval.system.bodies.append(self.player)

                self.evaluator= soPhysics.soPhysics(neweval.system)                
                #self.evaluator.system.moveToStar()
                self.loadPlanets()
                self.console = console
                self.toggleConsole()
                
                #if len(starList)>0:
                #        self.loadStars()
                base.camLens.setNear(0.01)
  #              base.camLens.setFar(50000)
		base.camLens.setFar(170000000000000000000000000000000000000)
         	self.mouselook=False
		self.loadLights()
		taskMgr.add(self.move,"move")

        def loadLights(self):
                plight = PointLight('plight')
                plight.setColor(VBase4(1, 1, 1, 1))
                plnp = render.attachNewNode(plight)
                plnp.setPos(0, 0, 0)
                render.setLight(plnp)


        
        def loadStars(self):
                print "loading stars"
                for star in self.stars:
                        star.body.node = render.attachNewNode(star.body.name)
                        star.body.sphere = loader.loadModelCopy("models/dodecahedron")			
                        star.body.sphere.reparentTo(star.body.node)
                        star.body.sphere.setScale(self.starScale)
                        star.body.node.setPos(star.body.position.x,star.body.position.y,star.body.position.z)
        def setTexture(self, body, i):
                if body.mass< 0.001:                       
                        body.texture = loader.loadTexture("models/pluto.jpg")
                elif body.mass >= 0.001 and body.mass < .002:
                        body.texture = loader.loadTexture("models/mercury.jpg")
                elif body.mass >= .002 and body.mass < .003:
                        body.texture = loader.loadTexture("models/venus.jpg")
                elif body.mass >= .003 and body.mass < .006:
                        body.texture = loader.loadTexture("models/earthmoon.jpg")
                elif body.mass >= .006 and body.mass < .009:
                        body.texture = loader.loadTexture("models/mars.jpg")
                elif body.mass >= .009 and body.mass < .01:
                        body.texture = loader.loadTexture("models/uranus.jpg")
                elif body.mass >= .01 and body.mass < .03:
                        body.texture = loader.loadTexture("models/saturn.jpg")
                elif body.mass >= .03 and body.mass < .05:
                        body.texture = loader.loadTexture("models/neptune.jpg")
                elif body.mass >= .05 and body.mass < .1:
                        body.texture = loader.loadTexture("models/saturn.jpg")
                elif body.mass >= .1 and body.mass < .4:
                        body.texture = loader.loadTexture("models/jupiter.jpg")
                elif body.mass >= .4:
                        body.texture = loader.loadTexture("models/sun.jpg")
                        sunMaterial =Material()
                        sunMaterial.setTwoside(True)
                        sunMaterial.setEmission(VBase4(1,1,1,1))
                        body.node.setMaterial(sunMaterial)
                #else:
                        #body.texture = loader.loadTexture("models/mars.jpg")
                body.sphere.setTexture(body.texture,1)

        def loadSinglePlanet(self, body,i):
                body.node = render.attachNewNode(body.name)
                if self.evaluator.gridSystem.names[i]!="player" and body.name != "player":
                        body.sphere = loader.loadModelCopy("models/planet_sphere")			
                        body.sphere.reparentTo(body.node)
                        self.scalebody( i)
##                        scaleRate = ((math.sqrt(self.evaluator.gridSystem.mass[i]))/100)+.01
##                        body.sphere.setScale(scaleRate)
##                        self.evaluator.gridSystem.rad[i]=scaleRate                                
##                        body.mass=self.evaluator.gridSystem.mass[i]
##                        self.setTexture(body, i)
                        body.node.setPos(self.evaluator.gridSystem.pos[i][0],
                                         self.evaluator.gridSystem.pos[i][1],
                                         self.evaluator.gridSystem.pos[i][2])

                else:
                        self.loadPlayer(body)
        def detachNode(self, i):
                #count = len(self.evaluator.system.bodies)-1
                print "detaching node: ",i#count
                self.evaluator.system.bodies[i].node.detachNode()
	def loadPlanets(self):
                
                pval = self.evaluator.gridSystem.player
                print "player: ",pval
                print self.evaluator.gridSystem.getPlayerIndex()
                i=0
                for body in self.evaluator.system.bodies:
                        if i ==pval:
                                print "player at: ",i 
                                self.loadPlayer(self.player)
                        if i != pval:
                                self.loadSinglePlanet(body,i)
                        i+=1
                self.sky = loader.loadModel("models/solar_sky_sphere")                               
                self.sky_tex = loader.loadTexture("models/startex.jpg")
                self.sky.setTexture(self.sky_tex, 1)
                self.sky.setScale(self.skyScale)
                self.sky.reparentTo(render)

                
        def scaleUp(self):
                self.accRate*= 1.01
                print "accRate increasing",self.accRate
##                print self.starScale
##                for star in self.stars:
##                        star.body.sphere.setScale(self.starScale)
                        
        def scaleDown(self):
                self.accRate*= .99
                print "accRate decreasing",self.accRate
##                print self.starScale
##                for star in self.stars:
##                        star.body.sphere.setScale(self.starScale)
                                                
	def toggleConsole(self):
                print "toggle console"
                self.console.toggle()

        def addPlanet(self):
                self.loadSinglePlanet(self.evaluator.system.addSinglePlanet())                
                return
        
	def loadRoid(self, abody):
                if(len(self.player.bodies)<10):
                        self.player.bodies.append(abody)
                        self.evaluator.system.bodies.append(abody)
                        self.evaluator.accelerateCuda()
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

	def loadPlayer(self, abody):
                abody.node = render.attachNewNode(abody.name)
                abody.model = loader.loadModelCopy("models/fighter")			
                abody.model.reparentTo(abody.node)
                if abody.name == "player":
                        abody.texture = loader.loadTexture("models/texturemap.png")
                elif abody.name == "mouse":
                        abody.texture = loader.loadTexture("models/sun.jpg")
                abody.model.setScale(.00005)
                abody.radius=.00005
                i = self.evaluator.gridSystem.getPlayerIndex()
                self.evaluator.gridSystem.rad[i]=0.01
                abody.node.setPos(self.evaluator.gridSystem.pos[i][0],
                                  self.evaluator.gridSystem.pos[i][1],
                                  self.evaluator.gridSystem.pos[i][2])

        def exit(self):
                quit()
                return
        def fullscreen(self):
                print "doh"
                             
	def move(self,task):
#                self.accept("p", self.addPlanet)
                self.accept("`", self.toggleConsole)
                self.accept("wheel_right", self.tiltLeft)
                self.accept("wheel_left", self.tiltRight)
#                self.accept("mouse6", self.tiltLeft)
#                self.accept("mouse7", self.tiltRight)
                self.accept("w", self.tiltLeft)
                self.accept("r", self.tiltRight)
                self.accept("mouse2", self.handlemouse2Click)
                #self.accept("mouse3", self.handleRightMouseClick)
                #self.accept("mouse1", self.handleLeftMouseClick)
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
		dt = self.dt
		if not self.mapMode:
                        self.evaluator.accelerateCuda()
		self.updateMouse(self.player)
		if self.starting: 
			dt=dt/2.0
			self.starting=False
		#self.reloadPlanets()
		self.setAllPositions()
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
                else:
                        self.mapMode=True
                        self.zoom = 59000
                        
	def accelerate(self):                                  
                print "accelerating ship"
                i = self.evaluator.gridSystem.getPlayerIndex()
                
                self.evaluator.gridSystem.acc[i][0]+=self.dX
                self.evaluator.gridSystem.acc[i][1]+=self.dY
                self.evaluator.gridSystem.acc[i][2]+=self.dZ
                self.evaluator.gridSystem.printBody(i)
                return
        
        def stop(self):
                i = self.evaluator.gridSystem.player
                print "stopping ship", i
                self.evaluator.gridSystem.printBody(i)
                self.evaluator.gridSystem.vel[i][0]=0.0
                self.evaluator.gridSystem.vel[i][1]=0.0
                self.evaluator.gridSystem.vel[i][2]=0.0
                return
        
        def brake(self):
                print "slowing ship"
                i = self.evaluator.gridSystem.player
                self.evaluator.gridSystem.printBody(i)
                self.evaluator.gridSystem.acc[i][0]-=self.dX
                self.evaluator.gridSystem.acc[i][1]-=self.dY
                self.evaluator.gridSystem.acc[i][2]-=self.dZ
                
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
                if (True):
                        newX=self.mouseX
                        newY=self.mouseY
                        if self.mouselook and base.mouseWatcherNode.hasMouse():
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
                cpos=self.evaluator.gridSystem.getPlayerIndex()
                #base.camera.printPos()
                base.camera.setPos(self.evaluator.gridSystem.pos[cpos][0]-self.dX,
                                   self.evaluator.gridSystem.pos[cpos][1]-self.dY,
                                   self.evaluator.gridSystem.pos[cpos][2]-self.dZ)

        def setAllPositions(self):
                for j in self.evaluator.gridSystem.collisions:
                        self.scalebody(j)
                self.evaluator.gridSystem.collisoins=[]

                for k in self.evaluator.gridSystem.removed:
                        self.detachNode(k)
##                        abody = Body(self.evaluator.system.getDirectedPlanet())
##                        self.evaluator.gridSystem.insertBody(abody,k)
##                        self.loadSinglePlanet(abody, k)
                self.evaluator.gridSystem.removed=[]

                
                i=0
                for body in self.evaluator.system.bodies:
                        self.set_body_position(body,
                                               self.evaluator.gridSystem.pos[i][0],
                                               self.evaluator.gridSystem.pos[i][1],
                                               self.evaluator.gridSystem.pos[i][2])
                        i+=1

        def scalebody(self, i):
                body = self.evaluator.system.bodies[i]
                if body.name == "player":
                        print "rescaling: ",i," ",body.name
                        raw_input()
                scaleRate = ((math.sqrt(self.evaluator.gridSystem.mass[i]))/50)+.001
                body.sphere.setScale(scaleRate)
                self.evaluator.gridSystem.rad[i]=scaleRate                                
                body.mass=self.evaluator.gridSystem.mass[i]
                self.setTexture(body, i)

	def set_body_position(self,body,x,y,z):
                body.node.setPos(x,y,z) 
                body.node.setHpr(body.orientation.x, body.orientation.y, body.orientation.z)
