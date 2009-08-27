import orbitSystem
import random
import dircache
import random
import math
import sys
import os
import copy
from ctypes import *

#cphysics = CDLL('sophysics.so')
#import pycuda.autoinit
#import pycuda.driver as drv
#import numpy
#import psyco
#psyco.full()

#add collision detection

#this is the cuda module

##mod = drv.SourceModule("""
##
##__global__ void accGravSingle(float *mass, float **pos, float **vel, float **acc, *rad, int ith, int  jth)
##{
##  float d_x = pos[jth][0] - pos[ith][0];
##  float d_y = pos[jth][1] - pos[ith][1];
##  float d_z = pos[jth][2] - pos[ith][2];
##  float radius = d_x**2 + d_y**2 + d_z**2;
##  float grav_mag = 0.0;
##  if (radius >0){
##    grav_mag = G/((radius+epsilon)**(3.0/2.0));
##  }
##  else{

#    radius = 0.001;
##    grav_mag = G/((radius+epsilon)**(3.0/2.0));
##   }
##
##   float grav_x=grav_mag*d_x;
##   float grav_y=grav_mag*d_y;
##   float grav_z=grav_mag*d_z;
##     
##   acc[ith][0] +=grav_x*mass[jth];
##   acc[ith][1] +=grav_y*mass[jth];
##   acc[ith][2] +=grav_z*mass[jth];
##
##   acc[jth][0] +=grav_x*mass[ith];
##   acc[jth][1] +=grav_y*mass[ith];
##   acc[jth][2] +=grav_z*mass[ith];   
##}
##""")
G=2.93558*10**-4
epsilon = 0.01
class soPhysics:
	def __init__(self,aSystem, maxMark=10000, dt=.02):
		self.dt=dt
		self.system = aSystem
		self.gridSystem = orbitSystem.GridSystem(aSystem.bodies)
		self.maxMark=maxMark
		self.fitness=self.system.evaluate()
		self.sumFit=self.system.evaluate()
		self.t=0
		self.count=1
		self.collisions=[]
		#self.gridSys = GridSystem(self.system.bodies)
		#self.accGravSingle = mod.get_function("accGravSingle")

	def collisionDetected(self, body1, body2):
                if body1.name == "player":
                        body1.position.z += 1
                        body1.velocity.x*=0.125
                        body1.velocity.y*=0.125
                        body1.velocity.z*=0.125

        def combineBodies(self, body1, body2):
                body3 = Body()
                body3.mass = body1.mass + body2.mass
                body3.position.x = body1.position.x + body2.position.x/2
                body3.position.y = body1.position.y
                body3.position.z = body1.position.z
                body3.velocity.x = (((body1.mass*body1.velocity.x)+
                                     (body2.mass*body2.velocity.x)/
                                     (body1.mass+body2.mass)))
                body3.velocity.y = (((body1.mass*body1.velocity.y)+
                                     (body2.mass*body2.velocity.y)/
                                     (body1.mass+body2.mass)))
                body3.velocity.z = (((body1.mass*body1.velocity.z)+
                                     (body2.mass*body2.velocity.z)/
                                     (body1.mass+body2.mass)))
                return body3
                        
	def evaluateStep(self):
                self.accelerate()
                for body in self.system.bodies:
                        self.calculate_velocity(body,self.dt)
                        self.calculate_position(body,self.dt)
                        body.acceleration.reset()
			self.sumFit+=self.system.evaluate()
			self.t+=self.dt
		self.count+=1

	def evaluate(self):
		self.t=0
		self.count=1
		self.accelerate()
		self.sumFit=0
		while self.count<self.maxMark:
                        self.evaluateStep()			
		self.fitness = self.system.evaluate()
		self.avgStability = self.sumFit/self.count
		return self.avgStability
	
	def accGravSingle(self, mass, pos, vel, acc, rad, ith, jth):
                d_x = pos[jth][0] - pos[ith][0]
                d_y = pos[jth][1] - pos[ith][1]
                d_z = pos[jth][2] - pos[ith][2]
                radius = d_x**2 + d_y**2 + d_z**2
                rad2 = math.sqrt(radius)
                grav_mag = 0.0;
                
                if (rad2 > rad[ith]+rad[jth]):
                        grav_mag = G/((radius+epsilon)**(3.0/2.0))
                else:
                        print "collision i ",ith," j ",jth
                        print rad2
                        grav_mag = 0
                              
                grav_x=grav_mag*d_x
                grav_y=grav_mag*d_y
                grav_z=grav_mag*d_z
                   
                acc[ith][0] +=grav_x*mass[jth]
                acc[ith][1] +=grav_y*mass[jth]
                acc[ith][2] +=grav_z*mass[jth]
                
                acc[jth][0] +=grav_x*mass[ith]
                acc[jth][1] +=grav_y*mass[ith]
                acc[jth][2] +=grav_z*mass[ith]   
                
	def accelerateCuda(self):
                G=2.93558*10**-4
		epsilon = 0.01
		for i in range(0,self.gridSystem.count):
			for j in range(0,i):
##                                self.accGravSingle(byref(self.gridSystem.mass),
##                                                   byref(self.gridSystem.pos),
##                                                   byref(self.gridSystem.vel),
##                                                   byref(self.gridSystem.acc),
##                                                   byref(self.gridSystem.rad),
##                                                   i, j)
                                self.accGravSingle(self.gridSystem.mass,
                                                   self.gridSystem.pos,
                                                   self.gridSystem.vel,
                                                   self.gridSystem.acc,
                                                   self.gridSystem.rad,
                                                   i, j)
                self.calVelPosCuda()
                self.gridSystem.resetAcc()
                
        def calVelPosCuda(self):
                for i in range(0,self.gridSystem.count):
                        self.gridSystem.vel[i][0]+=self.dt*self.gridSystem.acc[i][0]
                        self.gridSystem.vel[i][2]+=self.dt*self.gridSystem.acc[i][1]
                        self.gridSystem.vel[i][1]+=self.dt*self.gridSystem.acc[i][2]

                        self.gridSystem.pos[i][0]+=self.dt*self.gridSystem.vel[i][0]
                        self.gridSystem.pos[i][2]+=self.dt*self.gridSystem.vel[i][1]
                        self.gridSystem.pos[i][1]+=self.dt*self.gridSystem.vel[i][2]
