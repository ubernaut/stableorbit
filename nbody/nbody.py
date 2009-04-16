from ctypes import *
from bootstrap import *
import direct.directbase.DirectStart
from direct.task.Task import Task
#import psyco
import math
#psyco.full()
system = System()
nbody_c = CDLL('lib/libnbody.so')

panda_bodies = []
starting = True

class PandaBody(object):
  def __init__(self, data):
    self.node = data[0]
    self.sphere = data[1]

def read_data(file):
  file = open(file)
  for i,data in enumerate(file.readlines()):
    data = data.split(" ")
    system.bodies[i].mass = c_float(float(data[1]))
    system.bodies[i].position.x = c_float(float(data[2]))
    system.bodies[i].position.y = c_float(float(data[3]))
    system.bodies[i].position.z = c_float(float(data[4]))
    system.bodies[i].velocity.x = c_float(float(data[5]))
    system.bodies[i].velocity.y = c_float(float(data[6]))
    system.bodies[i].velocity.z = c_float(float(data[7]))
  system.N = 60
    
def add_test_particles():
  r = 3
  dr = .5
  G=0.000293558
  for body in system.bodies:
    if not body.mass:
      body.mass = c_float(0.0)
      body.position.x = c_float(r)
      body.position.y = c_float(0.0)
      body.position.z = c_float(0.0)
      body.velocity.x = c_float(0.0)
      body.velocity.y = c_float(math.sqrt(G/r))
      body.velocity.z = c_float(0.0)
      r += dr

def do_step(task, starting = False):
  dt = 0.1
  dt_c = c_float(0.1)
  nbody_c.do_step(byref(system), dt_c)
  for i,body in enumerate(system.bodies):
    p_body = panda_bodies[i]
    p_body.node.setPos(float(body.position.x), float(body.position.y), float(body.position.z))
  return task.cont
  

read_data('./data/initial_conditions.txt')

add_test_particles()
environ = loader.loadModel("models/solar_sky_sphere")
environ.reparentTo(render)
#environ_texture = loader.loadTexture("models/stars_1k_tex.jpg")
#environ.setTexture(environ_texture)
environ.setScale(100)
environ.setPos(0,0,0)
base.camera.setPos(0,-10,0)
for i,body in enumerate(system.bodies):
  panda_bodies.append(PandaBody([render.attachNewNode("body" + str(i)),loader.loadModelCopy("models/planet_sphere")]))
  p_body = panda_bodies[i]
  p_body.sphere.reparentTo(p_body.node)
  p_body.sphere.setScale(0.15*(1+body.mass))
  if body.mass == 0.0:
    p_body.texture = loader.loadTexture("models/neptune.jpg")
  else:
    p_body.texture = loader.loadTexture("models/mars.jpg")
  p_body.sphere.setTexture(p_body.texture,1)
  p_body.node.setPos(float(body.position.x), float(body.position.y), float(body.position.z))
taskMgr.add(do_step,'do_step')
run()
