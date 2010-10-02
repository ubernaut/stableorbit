import StarSystem
import random
import dircache
import random
import math
import sys
import os
import copy
from ctypes import *
G=2.93558*10**-4
epsilon = 0.01
class soPhysics:
	def __init__(self,aSystem, maxMark=100000, dt=.02):
		self.dt=dt
		self.system = aSystem
		self.gridSystem = orbitSystem.GridSystem(aSystem.bodies)
		self.maxMark=maxMark
		self.fitness=self.system.evaluate()
		self.sumFit=self.fitness#self.system.evaluate()
		self.t=0
		self.count=1
		self.collisions=[]
		#self.gridSys = GridSystem(self.system.bodies)
		#self.accGravSingle = mod.get_function("accGravSingle")

	def collisionDetected(self, player, names, mass,
                              pos, vel, acc, rad, ith, jth):
                #print "i: ",ith,"j: ",jth
##                if names[ith] == "player"and ith!=0 and player == ith:
##                        print "player hit: ", ith
##                        pos[ith][2] += 3
##                        vel[ith][0]=0
##                        vel[ith][1]=0
##                        vel[ith][2]=0
##                if names[jth] == "player" and jth!=0 and player == jth:
##                        print "player hit: ", jth
##                        pos[jth][2] += 3
##                        vel[jth][0]=0
##                        vel[jth][1]=0
##                        vel[jth][2]=0
                if (names[jth]!="player" and
                    names[ith]!="player"):# and
                    #ith != 0 and jth != 0):
                        print "combining ", ith," and ",jth
                        self.combineBodies(player, names, mass, pos,
                                           vel, acc, rad, ith, jth)


        def combineBodies(self, player, names, mass,
                              pos, vel, acc, rad, ith, jth):
                print "combining bodies i: ",ith,"j: ",jth
                self.gridSystem.printBody(ith)
                self.gridSystem.printBody(jth)
                
                pos[jth][0] = (pos[ith][0]*mass[ith] + pos[jth][0]*mass[jth])/((mass[ith]+mass[jth]))
                pos[jth][1] = (pos[ith][1]*mass[ith] + pos[jth][1]*mass[jth])/((mass[ith]+mass[jth]))
                pos[jth][2] = (pos[ith][2]*mass[ith] + pos[jth][2]*mass[jth])/((mass[ith]+mass[jth]))
                
                vel[jth][0] = (((mass[ith]*vel[ith][0])+
                                     (mass[jth]*vel[jth][0])/#2))
                                     ((mass[ith]+mass[jth]))))
                vel[jth][1] = (((mass[ith]*vel[ith][1])+
                                     (mass[jth]*vel[jth][1])/#2))
                                     ((mass[ith]+mass[jth]))))
                vel[jth][2] = (((mass[ith]*vel[ith][2])+
                                     (mass[jth]*vel[jth][2])/#2))
                                     ((mass[ith]+mass[jth]))))
                mass[jth] = mass[ith] + mass[jth]
                pos[ith][0]+=10
                pos[ith][1]+=10
                pos[ith][2]+=10
                names[ith]= "DELETE"
                self.gridSystem.collisions.append(jth)
                self.gridSystem.removed.append(ith)
                self.gridSystem.getPlayerIndex()

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
	
	def accGravSingle(self, player, names, mass,
                          pos, vel, acc, rad, ith, jth):
                d_x = pos[jth][0] - pos[ith][0]
                d_y = pos[jth][1] - pos[ith][1]
                d_z = pos[jth][2] - pos[ith][2]
                #if d_z >0:
                #        print "ith ",ith, "jth ",jth
                radius = d_x**2 + d_y**2 + d_z**2
                rad2 = math.sqrt(radius)
                grav_mag = 0.0;
                
                if (rad2 > rad[ith]+rad[jth]):
                        grav_mag = G/((radius+epsilon)**(3.0/2.0))
                        grav_x=grav_mag*d_x
                        grav_y=grav_mag*d_y
                        grav_z=grav_mag*d_z
                           
                        acc[ith][0] +=grav_x*mass[jth]
                        acc[ith][1] +=grav_y*mass[jth]
                        acc[ith][2] +=grav_z*mass[jth]
                        
                        acc[jth][0] +=grav_x*mass[ith]
                        acc[jth][1] +=grav_y*mass[ith]
                        acc[jth][2] +=grav_z*mass[ith]
                else:
                        
                        #print "collision i ",ith," j ",jth
                        #print "rad ",rad2
                        grav_mag = 0
                        self.collisionDetected(player, names, mass, pos,
                                               vel, acc, rad, ith, jth)

                              
   
                
	def accelerateCuda(self):
                G=2.93558*10**-4
		epsilon = 0.01
		for i in range(0,self.gridSystem.count):
			for j in range(0,i):

                                self.accGravSingle(self.gridSystem.player,
                                                   self.gridSystem.names,
                                                   self.gridSystem.mass,
                                                   self.gridSystem.pos,
                                                   self.gridSystem.vel,
                                                   self.gridSystem.acc,
                                                   self.gridSystem.rad,
                                                   i, j) 
                self.calVelPosCuda()
                self.gridSystem.resetAcc()
                for i in range(0,self.gridSystem.count):
                        if self.gridSystem.names[i]=="DELETE":
                                self.gridSystem.removeBody(i)
                #self.gridSystem.collisions = []
                
        def calVelPosCuda(self):
                for i in range(0,self.gridSystem.count):
                        self.gridSystem.vel[i][0]+=self.dt*self.gridSystem.acc[i][0]
                        self.gridSystem.vel[i][1]+=self.dt*self.gridSystem.acc[i][1]
                        self.gridSystem.vel[i][2]+=self.dt*self.gridSystem.acc[i][2]

                        self.gridSystem.pos[i][0]+=self.dt*self.gridSystem.vel[i][0]
                        self.gridSystem.pos[i][1]+=self.dt*self.gridSystem.vel[i][1]
                        self.gridSystem.pos[i][2]+=self.dt*self.gridSystem.vel[i][2]
