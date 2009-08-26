#! /usr/bin/python
from ctypes import *

import dircache
import os
import random
import dircache
import direct.directbase.DirectStart

from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import PointLight,Vec4
from direct.task.Task import Task
#gcc -o nbody.so -shared -fPIC nbody.c
nbody_c = CDLL('lib/nbody.so') 


class DirectBody(object):
  def __init__(self, body):
    self.c=body
    self.node = 0 
    self.texture = 0
    self.sphere = 0
    
class DSystem(object):
  def __init__(self):
    self.bodies = []

class Universe(DirectObject):
  def __init__(self, system):
    self.system_c = system
    self.system = DSystem()
    self.starting = True
    self.dt = 0.01
    self.load_planets(system)
    print 'hello from init'
    base.camLens.setFar(1000000000000)
    taskMgr.add(self.move,"move")
    self.start(self.system_c, self.dt)
    run()
  def start(self, system_c, dt):
    nbody_c.accelerate(byref(system_c))
    for body in system_c.bodies:
      print body.acceleration.x, body.acceleration.y. body.acceleration.z

  def load_planets(self, system):
    for body in system.bodies:
      body = DirectBody(body)                        
      body.node = render.attachNewNode(str(body.c.name))
      print body.node
      body.sphere = loader.loadModelCopy("models/planet_sphere")      
      body.sphere.reparentTo(body.node)
      body.sphere.setScale(0.1)
      body.texture = loader.loadTexture("models/mars.jpg")
      body.sphere.setTexture(body.texture,1)
      self.set_body_position(body)
      self.system.bodies.append(body)

  def move(self,task):
    dt = self.dt
    system = self.system
    system_c = self.system_c
    nbody_c.accelerate(byref(system_c))
    if self.starting: 
      dt=dt/2.0
      nbody_c.update_velocity(byref(system_c), c_float(dt))
      dt = dt*2.0
      self.starting=False
    else:
      nbody_c.update_velocity(byref(system_c), c_float(dt))
    nbody_c.update_position(byref(system_c), c_float(dt))
    for body in system.bodies:
      print body.c.position.x
      self.set_body_position(body)
    return Task.cont
  def set_body_position(self,body):
    body.node.setPos(float(body.c.position.x),float(body.c.position.y),float(body.c.position.z))
  

