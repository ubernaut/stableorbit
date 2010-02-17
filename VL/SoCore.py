#! /usr/bin/python
import dircache
import os
import random
import dircache
import StarSystem
import soPhysics
import math
from StarSystem import Body
from StarSystem import StarSystem
import interactiveConsole
from direct.filter.CommonFilters import CommonFilters
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

class SoInput(object):
        def __init__(self):
                self.mouselook=True
                self.zoom = .33
                self.mapMode = False
                self.hudScale = 1
		self.starting=True
		self.mouseX = 0
                self.mouseY = 0
                self.dX=0
                self.dY=0
                self.dZ=0
  		self.mouselook=False
  		
  	def updateMouse(self, abody, dobase):
                if (True):
                        newX=self.mouseX
                        newY=self.mouseY
                        if self.mouselook and base.mouseWatcherNode.hasMouse():
                                newX = dobase.mouseWatcherNode.getMouseX()
                                newY = dobase.mouseWatcherNode.getMouseY()                        
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
                                   abody.orientation.y, abody.orientation.z)
                #cpos=self.evaluator.gridSystem.getPlayerIndex()
                #base.camera.printPos()
                base.camera.setPos(abody.position.x-self.dX,
                                   abody.position.y-self.dY,
                                   abody.position.z-self.dZ)


        
class SoPlayer(object):
        def __init__(self):
                self.player = Body()
                self.player.name = "player"
		self.player.mass = 0
		self.player.position.x=0
		self.player.position.y=0
		self.player.position.z=-0.04
		self.player.orientation.y=90
		self.player.name = "player"
		self.player.mass = 0
		self.player.position.x=0
		self.player.position.y=0
		self.player.position.z=-0.04
		self.player.orientation.y=90
		self.starsys=StarSystem()
	def handleinput():
                return
        

                
from direct.showbase import DirectObject
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import PointLight,Vec4
from direct.task.Task import Task
import direct.directbase.DirectStart

class SoCore(DirectObject):
        def __init__(self,  console):
                self.starsystem=StarSystem()
                self.objectScale=.01
                self.starScale = 10
                self.skyScale=50000
		self.dt=.02
		self.player=SoPlayer()
		self.input=SoInput()
                base.camLens.setNear(0.01)
  		base.camLens.setFar(170000000000000000000000000000000000000)
  		self.loadLights()
  		self.loadPlayer(self.player.player)
  		self.load_body(Body())
  		self.console=console
  		taskMgr.add(self.move,"move")
#  	def steptime():
#                self.input.handleinput()
#                return


        def loadPlayer(self, abody):
                abody.node = render.attachNewNode(abody.name)
                abody.mass = 0.0001
                abody.model = loader.loadModelCopy("models/fighter")			
                abody.model.reparentTo(abody.node)
##                if abody.name == "player":
                abody.texture = loader.loadTexture("models/texturemap.png")
##                elif abody.name == "mouse":
##                        abody.texture = loader.loadTexture("models/sun.jpg")
                abody.model.setScale(.00005)
                abody.radius=.00005
                #i = self.evaluator.gridSystem.getPlayerIndex()
                abody.node.setPos(abody.position.x,
                                  abody.position.y,
                                  abody.position.z)
        
        def loadLights(self):
                plight = PointLight('plight')
                plight.setColor(VBase4(1, 1, 1, 1))
                self.plnp = render.attachNewNode(plight)
                self.plnp.setPos(0, 0, 0)
                render.setLight(self.plnp)

                self.ambientLight = AmbientLight( 'ambientLight' )
                self.ambientLight.setColor( Vec4( 0.91, 0.91, 0.91, 1 ) )
                
                self.ambientLightNP = render.attachNewNode( self.ambientLight.upcastToPandaNode() )
                render.setLight(self.ambientLightNP)
        def addObject(self, abody):
                abody.node = render.attachNewNode(abody.name)
                if abody.name!="player" and abody.name != "player":
                        abody.sphere = loader.loadModelCopy("models/planet_sphere")			
                        abody.sphere.reparentTo(abody.node)
#                        self.scalebody( i)
##                        scaleRate = ((math.sqrt(self.evaluator.gridSystem.mass[i]))/100)+.01
##                        body.sphere.setScale(scaleRate)
##                        self.evaluator.gridSystem.rad[i]=scaleRate                                
##                        body.mass=self.evaluator.gridSystem.mass[i]
##                        self.setTexture(body, i)
                        abody.node.setPos(abody.position.x,
                                         abody.position.y,
                                         abody.position.z)

                else:
                        self.loadPlayer(body)
	def toggleConsole(self):
                print "toggle console"
                self.console.toggle()
        def exit(self):
                quit()
                return
        def fullscreen(self):
                print "doh"
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
                                      
	def move(self,task):
#                self.accept("p", self.addPlanet)
                self.accept("`", self.toggleConsole)
#                self.accept("wheel_right", self.tiltLeft)
#                self.accept("wheel_left", self.tiltRight)
#                self.accept("mouse6", self.tiltLeft)
#                self.accept("mouse7", self.tiltRight)
#                self.accept("w", self.tiltLeft)
#                self.accept("r", self.tiltRight)
                self.accept("mouse2", self.handlemouse2Click)
                #self.accept("mouse3", self.handleRightMouseClick)
                #self.accept("mouse1", self.handleLeftMouseClick)
		self.accept("wheel_up", self.zoomIn)
		self.accept("wheel_down", self.zoomOut)
		self.accept("escape", self.exit)
#		self.accept("space",self.stop)
#		self.accept("d",self.brake)
#		self.accept("e",self.accelerate)
#		self.accept("f",self.fullscreen)
#		self.accept("m",self.togglemap)
#		self.accept("[",self.scaleDown)
#		self.accept("]",self.scaleUp)
#		self.accept("l",self.togglemouselook)
		dt = self.dt
		#if not self.input.mapMode# and self.evaluator != []:
                #        self.evaluator.accelerateCuda()
		self.input.updateMouse(self.player.player,base)
		#if self.starting: 
		#	dt=dt/2.0
		#	self.starting=False
		#self.reloadPlanets()
		#self.setAllPositions()
		self.set_body_position(self.player.player)
		return Task.cont
	

                        
	def tiltLeft(self):
                print "left"
                self.player.player.orientation.z-=10
        def tiltRight(self):
                print "right"
                self.player.player.orientation.z+=10
	def togglemouselook(self):
                print "toggling mouselook"
                if self.input.mouselook:
                        self.input.mouselook = False
                else:
                        self.input.mouselook = True

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
                self.input.zoom*=0.9
                print self.input.zoom
                #self.scaleDown()
                return
        
        def zoomOut(self):
                self.input.zoom*=1.1
                print self.input.zoom
                #self.scaleUp()
                if self.input.zoom > 60000:
                        self.input.zoomIn()
                return
        def loadSol(self):
                abody = Body()
        def load_body(self, abody):
                #self.player.bodies.append(abody)
                #self.evaluator.system.bodies.append(abody)
                #self.evaluator.accelerateCuda()
                abody.node = render.attachNewNode(abody.name)
                abody.model = loader.loadModelCopy("models/planet_sphere")			
                abody.model.reparentTo(abody.node)
                #abody.texture =
                self.scalebody(abody)
                abody.model.setColor(abody.material.color[0],abody.material.color[1],abody.material.color[2],abody.material.color[3])#Texture("models/sun.jpg")
                abody.model.setScale(abody.radius)
                abody.node.setPos(abody.position.x ,abody.position.y ,abody.position.z)
                return
        def scalebody(self, abody):
                #abody = self.evaluator.system.bodies[i]
                if abody.name == "player":
                        print "rescaling: "," ",body.name
                        raw_input()
                scaleRate = ((math.sqrt(abody.mass))/50)+.001
                abody.model.setScale(scaleRate)
                abody.radius=scaleRate                                


	def set_body_position(self,abody):
                if abody.name == "star":
                        #print "moving light"
                        self.plnp.setPos(x,y,z)                        
                abody.node.setPos(abody.position.x,abody.position.y,abody.position.z) 
                abody.node.setHpr(abody.orientation.x, abody.orientation.y, abody.orientation.z)
