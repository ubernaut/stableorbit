import orbitSystem
import Eval
import sxr_server
import random
import os
import psyco
psyco.full()
from Eval import Eval
from orbitSystem import System

class GeneticAlgorithm:
	def __init__(self):
		self.population =[]
		self.maxMark = 100000;
		self.popSize = 5
		self.alphaRate= 1
		while len(self.population)<self.popSize:
			aSystem=System(len(self.population))
			while aSystem.evaluate(aSystem.bodies)<-.3:
				aSystem.mutate(1,1,1)
			self.population.append(aSystem)
		self.nextGen = []
		self.currMark=0
		self.markN()
		
	def initFirstGen(self):
		val_checker=[]
		self.nextGen=[]
		for system in self.population:
			val_checker.append(system.avgStability)
		val_checker=sorted(val_checker)
		for system in self.population:
			sys=0
			if system.avgStability > -0.3 :
				self.nextGen.append(copy.deepcopy(system))
				sys = len(self.nextGen)		
			else:
				system.mutate(1,1,1)

	def markN(self):
		print "get N systems which pass the initial viral thm"
		#self.initFirstGen
		for mark in range (0,self.maxMark):
			self.alphaRate= 0.2/(mark**(9/10))
			if mark%100 == 0:
                                print "compute viral fitness for "+`mark`+" dt iterations"
			sysVar =0
			for aSystem in self.population:
				folder ="mark-"+`mark`+"sys-"+`sysVar`
				clientProc = Eval(aSystem,mark)
				fitness=clientProc.evaluate()
				if fitness > -.3 :
					self.nextGen.append(aSystem)
					if mark%1000 == 0:
						
						self.write_conditions( aSystem,folder)
						sysVar+=1
				else:
					newSys= copy.deepcopy(aSystem)
					newSys.mutate(self.alphaRate,self.alphaRate,self.alphaRate)
					self.population.append(newSys)
					
			while len(self.nextGen)<self.popSize:
				nexGenIndex = random.randInt(0,len(self.nextGen)-1)
				newSys= copy.deepcopy(self.nextGen[nexGenIndex])
				newSys.mutate(self.alphaRate,self.alphaRate,self.alphaRate)
				clientProc = Eval(newSys,mark)
				fitness=clientProc.evaluate()
				if fitness> -.3:
					self.population.append(newSys)
				
	def write_conditions(self,system,folder):
		os.chdir("data")
		os.mkdir(folder)
		os.chdir(folder)
		print"recording a mark:"+folder
		
		for body in system.bodies:
			pos=body.position
			vel=body.velocity
			data_file = open(body.name,"w+")
			data_file.write(str(body.mass)+"\t"+str(pos.x)+"\t"+str(pos.y)+"\t"+str(pos.z)+"\t"+str(vel.x)+"\t"+str(vel.y)+"\t"+str(vel.z) +"\n")
		os.chdir("..")
		os.chdir("..")
def runGA():
        GA = GeneticAlgorithm()
        GA.initFirstGen()
        GA.markN()
runGA()
