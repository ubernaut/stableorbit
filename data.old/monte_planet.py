#! /usr/bin/python

import dircache

#import psyco

import random

#psyco.full()


bodies={}

        
class Body(object):
	def __init__ (self,body_data):
		self.name=body_data[0]
		self.mass=float(body_data[1])
		self.position=Position(body_data[2:5])
		self.velocity=Velocity(body_data[5:8])
		self.acceleration=Acceleration()
		self.data_file=open('./data/' + self.name + '.txt', 'w')
	
	def __del__(self):
		del self.position
		del self.velocity
		del self.acceleration
		

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


class Control:
	def __init__(self,dt):
		self.max_distance=0.0
		self.set_max()
		self.start_leap_frog(dt)
		self.step(dt)
		
	
	def start_leap_frog(self,dt):
		self.accelerate()
		for body in bodies.values():
			body.velocity.x+=dt/2.0*body.acceleration.x
			body.velocity.y+=dt/2.0*body.acceleration.y
			body.velocity.z+=dt/2.0*body.acceleration.z
		
			body.acceleration.x=0.0
			body.acceleration.y=0.0
			body.acceleration.z=0.0

			body.position.x+=dt*body.velocity.x
			body.position.y+=dt*body.velocity.y
			body.position.z+=dt*body.velocity.z


	def step(self,dt):
		t=0
		t_max=100.0
		write=0

		while t<t_max:
			if not len(bodies):
				exit()
			
			self.accelerate()
			self.update(dt)
			#if write >10:
			#	write=0
			self.write_data()
			print t/t_max

			t+=dt
			write+=1
			

		for body in bodies.values():
			body.data_file.close()
			
	def accelerate(self):
		accel=bodies.values()
		G=2.93558*10**-4
		for i in range(0,len(accel)):
			current_body=accel[i]
			current_position=current_body.position
			for j in range(0,i):
				other_body=accel[j]
				other_position=other_body.position
			
				d_x=(other_position.x-current_position.x)
				d_y=(other_position.y-current_position.y)
				d_z=(other_position.z-current_position.z)
			
				radius = d_x**2 + d_y**2 + d_z**2
				
				print radius
				
				grav_mag = G/(radius**(3.0/2.0))
				
				grav_x=grav_mag*d_x
				grav_y=grav_mag*d_y
				grav_z=grav_mag*d_z
				
				current_body.acceleration.x += grav_x*other_body.mass
				other_body.acceleration.x -= grav_x*current_body.mass
				
				current_body.acceleration.y += grav_y*other_body.mass
				other_body.acceleration.y -= grav_y*current_body.mass
				
				current_body.acceleration.z += grav_z*other_body.mass
				other_body.acceleration.z -= grav_z*current_body.mass


				
	def set_max(self):
		for body in bodies.values():
			dist = (body.position.x**2 + body.position.y**2 + body.position.z**2)
			if dist > self.max_distance:
				self.max_distance = dist

			
	def update(self,dt):
		for body in bodies.values():
			dist = (body.position.x**2 + body.position.y**2 + body.position.z**2)
			
			body.velocity.x+=dt*body.acceleration.x
			body.velocity.y+=dt*body.acceleration.y
			body.velocity.z+=dt*body.acceleration.z
		
			body.acceleration.x=0.0
			body.acceleration.y=0.0
			body.acceleration.z=0.0

			body.position.x+=dt*body.velocity.x
			body.position.y+=dt*body.velocity.y
			body.position.z+=dt*body.velocity.z
			
			if dist > 50000:
				print body.name + " blew up"
				del bodies[body.name]
				del body
				print bodies.keys()



	
	def write_data(self):
		for body in bodies.values():
			body.data_file.write(str(body.position.x) + '\t' + str(body.position.y) + '\t' + str(body.position.z) + '\n')

	
			
			
class SolarConstructor:
	def __init__(self):
		self.build()
	
	def build(self):
		N=random.randint(55,125)
		bodies["MASSIVE"]=Body(["MASSIVE",100,0,0,0,0,0,0])
		for i in range(0,N):
			body_data=[]
			body_data.append("body_" + str(i))
			body_data.append(random.uniform(.1,10))
			for j in range(0,3):
				body_data.append(random.uniform(-150,150))
			for j in range(0,3):
				body_data.append(random.uniform(-0.051,0.051))
			
			body=Body(body_data)
			bodies[body.name]=body
		print len(bodies)
		

def light_sim():
	bodies["MASSIVE"]=Body(["MASSIVE",100,0,0,0,0,0,0])
	body_data=[]
	body_data.append("body_" + str(1))
	body_data.append(0.0)
	body_data.append(50)
	body_data.append(3)
	body_data.append(0)
	body_data.append(-172)
	body_data.append(0)
	body_data.append(0)
	body=Body(body_data)
	bodies[body.name]=body
	

#def set_conditions():
	#file = open('./initial_conditions/conditions.txt').readlines()
	#for line in file:
	#	body_data = line.split()
	#	body=Body(body_data)
	#	bodies[body.name]=body
	
#set_conditions()				
#C = SolarConstructor()
light_sim()
s=Control(0.00010)




	

