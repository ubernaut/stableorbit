#! /usr/bin/python

import direct.directbase.DirectStart

from direct.task import Task
from direct.actor import Actor
from direct.interval.IntervalGlobal import *
import math


from Numeric import *
import time
from threading import *
import dircache


bodies={}
accel=[]

class Scene():

        
class Body(object):
	def __init__ (self,body_data):
		self.name=body_data[0]
		self.mass=float(body_data[1])
		self.position=Position(body_data[2:5])
		self.velocity=Velocity(body_data[5:8])
		self.acceleration=Acceleration()
		self.data_file=open('./data/' + self.name + '.txt', 'w')

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


class ControlThread(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.step()

	def step(self):
		g=Gnuplot.Gnuplot(debug=1)
		g.title("a fucking example")
		t=0
		t_max=100000
		dt=0.01
		write=0
		
		self.accelerate()
		
		for name in bodies.keys():
			BodyThread(name,dt/2.0).update_velocity()
		
		while t<t_max:
			for name in bodies.keys():
				position=bodies[name].position
				BodyThread(name,dt).update_position()

			g.splot([[body.position.x,body.position.y,body.position.z] for body in bodies.values()])

		
			self.accelerate()
			
			for name in bodies.keys():
				BodyThread(name,dt).update_velocity()
			
			if write == 1000:
				print t/t_max*100, "Percent"
				for name in bodies.keys():
					BodyThread(name).write_data()
				write=0

			t+=dt
			write +=1
		
		for body in bodies.values():
			body.data_file.close()
			
	def accelerate(self):
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

		
class BodyThread(Thread):
	def __init__(self,name,dt=0):
		self.dt=dt
		self.name=name
		Thread.__init__(self)
			
	def update_position(self):
		dt=self.dt
		body=bodies[self.name]
		body.position.x+=dt*body.velocity.x
		body.position.y+=dt*body.velocity.y
		body.position.z+=dt*body.velocity.z

	def update_velocity(self):
		dt=self.dt
		body=bodies[self.name]
		body.velocity.x+=dt*body.acceleration.x
		body.velocity.y+=dt*body.acceleration.y
		body.velocity.z+=dt*body.acceleration.z
		
		body.acceleration.x=0.0
		body.acceleration.y=0.0
		body.acceleration.z=0.0

	
	def write_data(self):
		body=bodies[self.name]
		body.data_file.write(str(body.position.x) + '\t' + str(body.position.y) + '\t' + str(body.position.z) + '\n')

					
	
def set_conditions():
	file = open('./initial_conditions/conditions.txt').readlines()
	for line in file:
		body_data = line.split()
		body=Body(body_data)
		bodies[body.name]=body
		accel.append(body)
				



set_conditions()
ControlThread().start()




	

