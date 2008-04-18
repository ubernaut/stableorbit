#! /usr/bin/python
import dircache
#import psyco
#psyco.full()

import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task

bodies={}

class Body(object):
	def __init__(self,name,body_data):
		self.name=name
		self.sphere=""
		self.node=""
		self.time={}
		for i,line in enumerate(body):
	 		position_data = line.split()
	 		self.time[i]=BodyPosition(position_data)


class BodyPosition(object):
	def __init__(self,position_data):
		self.x=float(position_data[0])
		self.y=float(position_data[1])
		self.z=float(position_data[2])
		
		

class Universe(DirectObject):
	def __init__(self):
		base.setBackgroundColor(0,0,0)
		self.loadPlanets()
		self.time=0
		taskMgr.add(self.animate, "animate")

	def loadPlanets(self):
		texture=loader.loadTexture("models/jupiter.jpg")
		
		for body in bodies.values():
			pos=body.time[0]
			
			body.node = render.attachNewNode(body.name)
			body.sphere = loader.loadModelCopy("models/planet_sphere")			
			
			body.sphere.reparentTo(body.node)

			body.sphere.setTexture(texture,1)
			
			body.node.setPos(pos.x,pos.y,pos.z)

		#self.sky = loader.loadModel("models/solar_sky_sphere")
		#self.sky_tex = loader.loadTexture("models/stars_1k_tex.jpg")
		#self.sky.setTexture(self.sky_tex, 1)
		#self.sky.reparentTo(render)
		#self.sky.setScale(1000)
	
	def animate(self,task):
		time=self.time
		time_out=[]
		for body in bodies.values():
			try:
				pos = body.time[time]
				body.node.setPos(pos.x,pos.y,pos.z)
			except: 
				time_out.append(body)
				if len(time_out)==len(bodies):
					self.time=0
		self.time+=1
		if self.time>10000:
			self.time=0
		return Task.cont
		

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

	
set_conditions('data/system_7/')	
U=Universe()			
run()
