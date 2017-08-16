import random
import dircache
import math

class Body(object):
        def __init__ (self,body_data=[]):
                if body_data == []:
                        body_data=["body",1,0,0,0,0,0,0,0,0,0]
                self.name=body_data[0]
                self.mass=float(body_data[1])
                self.position=Point(body_data[2:5])
                self.velocity=Point(body_data[5:8])
                self.acceleration=Point(body_data[5:8])
                self.orientation=Point()
                self.angVelocity=Point()
                self.acceleration.reset()
                self.radius=.03

        def __del__(self):
                del self.name
                del self.mass
                del self.position
                del self.velocity
                del self.acceleration
                del self.orientation
                del self.angVelocity
                del self.radius
class MaterialBody(Body):
        def __init__(self, body_data=[], material=""):
                self.body = Body(bodydata)
                self.material = Material(material)
class Point(object):
        def __init__(self, position_data=[0,0,0]):
                self.x=float(position_data[0])
                self.y=float(position_data[1])
                self.z=float(position_data[2])
        def reset(self):
                self.x=0
                self.y=0
                self.z=0

class Galaxy(object):
    def __init__(self):
        self.stars = []
        self.theta = 0
        self.dTheta = .05
        self.maxTheta = 10
        self.alpha = 2000
        self.beta = 0.25
        self.e = 2.71828182845904523536
        self.starDensity = 1
        while self.theta< self.maxTheta:
            self.theta+=self.dTheta
            randRange = 2000/(1+self.theta/2)
            self.starDensity = 10/(1+self.theta/2)
            for i in range(0,int(self.starDensity)):
                xPos = self.alpha*(self.e**(self.beta*self.theta))*math.cos(self.theta)
                yPos = self.alpha*(self.e**(self.beta*self.theta))*math.sin(self.theta)
                xPos+=random.uniform(-randRange,randRange)
                yPos+=random.uniform(-randRange,randRange)
                zPos = random.uniform(-randRange,randRange)
                newStar = Star(xPos,yPos,zPos, "star", "cos")
                newStar2 = Star(-xPos,-yPos,-zPos, "star", "cos")
                self.stars.append(newStar)
                self.stars.append(newStar2)


class Star(object):
            def __init__(self, xPos=30000, yPos=0, zPos=0, player="duh", aName="default"):
                self.body = Body(["body",1,xPos,yPos,zPos,0,0,0,0,0,0])
                self.color = [0.0,0.0,1.0]
                self.mass = 16
                self.radius = 6.6
                self.temp= 33000
                self.buildrandom()
                #self.player = Player()
            def buildrandom(self):
                starrand = random.uniform(1,10000)
                if (starrand < 7600):
                        self.mtype()
                if (starrand < 8800  and starrand > 7600):
                        self.ktype()
                if (starrand < 9400 and starrand > 8800):
                        self.gtype()
                if (starrand < 9700 and starrand > 9400):
                        self.ftype()
                if (starrand < 9800 and starrand > 9900):
                        self.atype()
                if (starrand < 9900 and starrand > 9950):
                        self.btype()
                if (starrand < 9950):
                        self.otype()


            def otype(self):
                self.color = [1.0,0.0,0.0]
        #                self.color = [0.0,0.0,1.0,1.0]
                self.mass = 16
                self.radius = 6.6
                self.temp= 33000
            def btype(self):
                self.color = [0.5,0.5,0.8,1.0]
                #self.color = [1.0,0.0,0.0]
                self.mass = 2.1
                self.radius = 1.8
                self.temp= 10,000
            def atype(self):
                self.color = [1.0,1.0,1.0,1.0]
               #self.color = [1.0,0.0,0.0]
                self.mass = 1.4
                self.radius = 1.4
                self.temp= 7500
            def ftype(self):
                self.color = [1.0,1.0,0.8,1.0]
                self.color = [1.0,0.0,0.0]
                self.mass = 1
                self.radius = 1
                self.temp= 6000
            def gtype(self):
        #                self.color = [1.0,0.0,0.0]
                self.color = [1.0,1.0,0.0,1.0]
                self.mass = .8
                self.radius = 0.9
                self.temp= 5200
            def ktype(self):
                #self.color = [1.0,0.0,0.0]
                self.color = [1.0,0.2,0.2,1.0]
                self.mass = .7
                self.radius = 0.5
                self.temp= 3700
            def mtype(self):
                    self.color = [1.0,0.0,0.0,1.0]
                    #self.color = [1.0,0.0,0.0]
                    self.mass = .2
                    self.radius = .2
                    self.temp= 2000


#defaultSystem=System(1,1,32,.5,.03)

class System(object):
        def __init__(self, seed=1, starcount=1,
                     bodycount=1, abodyDistance=.5, abodySpeed=0.03):
                random.seed = seed
                self.seed = seed
                self.star = Star()
                self.starCount=starcount
                self.bodyCount= bodycount
                self.bodies=[]
                self.bodyDistance = abodyDistance
                self.bodySpeed = abodySpeed
                if seed !=0:
                        self.build()
                else:
                        self.buildSol()
                print "bodyCount: "+`len(self.bodies)`
                self.stability = 0.5 - self.evaluate()
                self.printed=False
                self.avgStability=0.5 - self.evaluate()
        def makeDefault(self):
                System(1,1,32,.5,.03)
        def moveToStar(self):
                for body in self.bodies:
                        body.position.x += self.star.body.position.x
                        body.position.y += self.star.body.position.y
                        body.position.z += self.star.body.position.z
        def getStar(self, body_data):
                body_data.append(random.uniform(.4,1))
                for j in range(0,2):
                        body_data.append(0.0)
                body_data.append(0.0)
                for j in range(0,2):
                        body_data.append(0.0)
                body_data.append(0.0)
                return body_data

        def getSymPlanets(self):
                body_data=[]
                body_data.append("body_X")
                body_data.append(random.uniform(.000001,.4))

                if quadrantVar > 0:
                        body_data.append(random.uniform(0,self.bodyDistance))
                        body_data.append(random.uniform(0,self.bodyDistance))
                        body_data.append(0.0)
                        body_data.append(random.uniform(0,self.bodySpeed))
                        body_data.append(random.uniform(-self.bodySpeed,0))
                        body_data.append(0.0)

                if quadrantVar< 0:
                        body_data.append(random.uniform(-self.bodyDistance,0))
                        body_data.append(random.uniform(-self.bodyDistance,0))
                        body_data.append(0.0)
                        body_data.append(random.uniform(-self.bodySpeed,0))
                        body_data.append(random.uniform(0,self.bodySpeed))
                        body_data.append(0.0)

        def getDirectedPlanet(self):
                quadrantVar =1
                body_data=[]
                body_data.append("body_X")
                body_data.append(random.uniform(.000001,.01))

                if quadrantVar > 0:
                        body_data.append(random.uniform(0,self.bodyDistance))
                        body_data.append(random.uniform(0,self.bodyDistance))
                        body_data.append(random.uniform(0,self.bodyDistance/64))
                if quadrantVar< 0:
                        body_data.append(random.uniform(-self.bodyDistance,0))
                        body_data.append(random.uniform(-self.bodyDistance,0))
                        body_data.append(random.uniform(-self.bodyDistance/64,0))

                if quadrantVar > 0:
                        body_data.append(random.uniform(0,self.bodySpeed))
                        body_data.append(random.uniform(-self.bodySpeed,0))
                        body_data.append(random.uniform(0,self.bodySpeed/32))
                if quadrantVar < 0:
                        body_data.append(random.uniform(-self.bodySpeed,0))
                        body_data.append(random.uniform(0,self.bodySpeed))
                        body_data.append(random.uniform(-self.bodySpeed/32),0)



                return body_data

        def getPlanet(self, body_data):
                body_data.append(random.uniform(.000001,.01))
                for j in range(0,2):
                        body_data.append(random.uniform(-self.bodyDistance,self.bodyDistance))
                body_data.append(0.0)
                for j in range(0,2):
                        body_data.append(random.uniform(-self.bodySpeed,self.bodySpeed))
                body_data.append(0.0)
                return body_data

        def buildSol(self):
                self.bodies=[]
                body_data=["Sol",1,0,0,0,0,0,0,0,0,0]
                self.bodies.append(Body(body_data))
                body_data=["Earth",0.000003,0,1,0,.04,0,0,0,0,0]
                self.bodies.append(Body(body_data))

        def build(self):
                for i in range(0,self.bodyCount):
                        if i < self.starCount:
                                self.addStar()
                        else:
                                self.addSinglePlanet()
        def addStar(self):
                body_data = self.getStar(["star"])
                body = Body(body_data)
                self.bodies.append(body)
        def reverseBody(self, adata):
                bdata = adata
                bdata[2]= 0 - adata[2]
                bdata[3]= 0 - adata[3]
                bdata[4]= 0 - adata[4]
                bdata[5]= 0 - adata[5]
                bdata[6]= 0 - adata[6]
                bdata[7]= 0 - adata[7]
                return bdata

        def addSinglePlanet(self):
                print "adding Body"
                body_data = self.getDirectedPlanet()
                aBody = Body(body_data)
                bBody = Body(self.reverseBody(body_data))
                otherBodies = []
                otherBodies.append(self.bodies[0])
                otherBodies.append(aBody)
                otherBodies.append(bBody)
                fitness = self.evaluateN(otherBodies)
                while fitness<.1 or fitness>1:
                        print "testing configuration"
                        adata = self.getDirectedPlanet()
                        aBody = Body(adata)
                        bdata = self.reverseBody(adata)
                        bBody = Body(bdata)
                        otherBodies = []
                        otherBodies.append(self.bodies[0])
                        otherBodies.append(aBody)
                        otherBodies.append(bBody)
                        fitness=self.evaluateN(otherBodies)
                self.bodies.append(aBody)
                self.bodies.append(bBody)
                return aBody

        def addPlanet(self):
                print "adding body"
                body_data = []
                body_data.append("body_X")
                body_data = self.getPlanet(body_data)
                aBody = Body(body_data)
                self.bodies.append(aBody)
                print "new stability"
                print self.evaluate()
                while self.evaluate()>1:
                        self.bodies.pop()
                        self.addPlanet()
                return


        def evaluate(self):
                kinetic=0.0
                potential=0.0
                G=2.93558*10**-4
                for body in self.bodies:
                        vel = body.velocity
                        vel_sq = (vel.x**2 + vel.y**2 + vel.z**2)
                        kinetic += 0.5*body.mass*vel_sq
                for i in range(0,len(self.bodies)):
                        current_body=self.bodies[i]
                        current_position=current_body.position
                        for j in range(0,i):
                                other_body=self.bodies[j]
                                other_position=other_body.position
                                d_x=(other_position.x-current_position.x)
                                d_y=(other_position.y-current_position.y)
                                d_z=(other_position.z-current_position.z)
                                radius = (d_x**2 + d_y**2 + d_z**2)**(0.5)
                                if radius >0 :
                                        potential -= G*current_body.mass*other_body.mass/radius
                try:
                        return abs(kinetic/potential)
                except:
                        return 100
        def evaluateN(self, somebodies):
                tempSys = System()
                tempSys.bodies = somebodies
                tempEval = soPhysics(tempSys,1000000,.01)
                return tempEval.sumFit

        def evaluateBodies(self, someBodies):
                kinetic=0.0
                potential=0.0
                G=2.93558*10**-4
                for body in someBodies:
                        vel = body.velocity
                        vel_sq = (vel.x**2 + vel.y**2 + vel.z**2)
                        kinetic += 0.5*body.mass*vel_sq
                for i in range(0,len(someBodies)):
                        current_body=someBodies[i]
                        current_position=current_body.position
                        for j in range(0,i):
                                other_body=someBodies[j]
                                other_position=other_body.position
                                d_x=(other_position.x-current_position.x)
                                d_y=(other_position.y-current_position.y)
                                d_z=(other_position.z-current_position.z)
                                radius = (d_x**2 + d_y**2 + d_z**2)**(0.5)
                                if radius >0 :
                                        potential -= G*current_body.mass*other_body.mass/radius
                try:
                        return abs(kinetic/potential)
                except:
                        return 100.0
        def bodies(self):
                return self.bodies


class GridSystem(object):
        def convert(data):
                tempDATA = []
                for i in data:
                        tempDATA.append([float(j) for j in i.split()])
                return array(tempDATA)

        def __init__(self, bodies=[]):
                self.count = len(bodies)
                N = self.count
                self.player=0
                self.names = [""]
                self.mass= [0.0]
                self.rad = [0.0]
                self.pos = [[0.0,0.0,0.0]]
                self.ori = [[0.0,0.0,0.0]]
                self.vel = [[0.0,0.0,0.0]]
                self.acc = [[0.0,0.0,0.0]]
                self.allocated =1
                self.collisions = []
                self.removed=[]
                for i in range (0,self.count):
                        self.addSpace()
                i = 0
                for body in bodies:
                        if body.name == "player":
                                self.player = i
                        self.insertBody(body, i)

                        i+=1

                for i in range (0,self.count):
                        self.printBody(i)
        def getPlayerIndex(self):
                i=0
                lasti = 0
                for name in self.names:
                        if name == "player":
                                self.player = i
                                lasti=i
                                return i
                        else:
                                i+=1
                return i

        def append(self, body):
                print "appending: ", self.count
                print "allocated: ", self.allocated

        def insertBody(self,body, i):
                self.names[i] = body.name
                self.mass[i] = body.mass
                self.rad[i] = body.radius
                self.pos[i][0] = body.position.x
                self.pos[i][1] = body.position.y
                self.pos[i][2] = body.position.z

                self.ori[i][0] = body.orientation.x
                self.ori[i][1] = body.orientation.y
                self.ori[i][2] = body.orientation.z

                self.vel[i][0] = body.velocity.x
                self.vel[i][1] = body.velocity.y
                self.vel[i][2] = body.velocity.z

                self.acc[i][0] = body.acceleration.x
                self.acc[i][1] = body.acceleration.y
                self.acc[i][2] = body.acceleration.z

        def printBody(self, i):
                print "printing body: ", i
                print "nam :",self.names[i]
                print "mas :",self.mass[i]
                print "rad :",self.rad[i]
                print "pos :",self.pos[i]
                print "vel :",self.vel[i]
                print "acc :",self.acc[i]

        def moveBody(self,source,dest):
                self.names[dest]=self.names[source]
                self.mass[dest]=self.mass[source]
                self.rad[dest]=self.rad[source]
                self.pos[dest]=self.pos[source]
                self.ori[dest]=self.ori[source]
                self.vel[dest]=self.vel[source]
                self.acc[dest]=self.acc[source]
                self.names[source]="OLD"


        def removeBody(self, i):
                if i != self.player:
                        if i == self.count -1:
                                foo=1

                        else:
                                self.moveBody(self.count-1, i)
                        self.count -=1
                        self.getPlayerIndex()


        def resetAcc(self):
                for i in range (0, self.count):
                    self.acc[i] = [0.0,0.0,0.0]

        def addSpace(self):
                self.allocated +=1
                self.names.append("")
                self.mass.append(0.0)
                self.rad.append(0.0)
                self.pos.append([0.0,0.0,0.0])
                self.ori.append([0.0,0.0,0.0])
                self.vel.append([0.0,0.0,0.0])
                self.acc.append([0.0,0.0,0.0])
G=2.93558*10**-4
epsilon = 0.01
class soPhysics:
        def __init__(self,aSystem, maxMark=100000, dt=.02):
                self.dt=dt
                self.system = aSystem
                self.gridSystem = GridSystem(aSystem.bodies)
                self.maxMark=maxMark
                self.fitness=self.system.evaluate()
                self.sumFit=self.fitness
                self.t=0
                self.count=1
                self.collisions=[]

        def collisionDetected(self, player, names, mass,
                              pos, vel, acc, rad, ith, jth):
                if (names[jth]!="player" and
                    names[ith]!="player"):
                        self.combineBodies(player, names, mass, pos,
                                           vel, acc, rad, ith, jth)


        def combineBodies(self, player, names, mass,
                              pos, vel, acc, rad, ith, jth):
                pos[jth][0] = (pos[ith][0]*mass[ith] + pos[jth][0]*mass[jth])/((mass[ith]+mass[jth]))
                pos[jth][1] = (pos[ith][1]*mass[ith] + pos[jth][1]*mass[jth])/((mass[ith]+mass[jth]))
                pos[jth][2] = (pos[ith][2]*mass[ith] + pos[jth][2]*mass[jth])/((mass[ith]+mass[jth]))

                vel[jth][0] = (((mass[ith]*vel[ith][0])+(mass[jth]*vel[jth][0])/((mass[ith]+mass[jth]))))
                vel[jth][1] = (((mass[ith]*vel[ith][1])+(mass[jth]*vel[jth][1])/((mass[ith]+mass[jth]))))
                vel[jth][2] = (((mass[ith]*vel[ith][2])+(mass[jth]*vel[jth][2])/((mass[ith]+mass[jth]))))

                mass[jth] = mass[ith] + mass[jth]
                mass[ith] = 0.00000000000000000000000000000000000000000000000001
                pos[ith][0]=10
                pos[ith][1]=10
                pos[ith][2]=10

                vel[ith][0]=0
                vel[ith][1]=0
                vel[ith][2]=0
                names[ith]= "DELETED"
                self.gridSystem.collisions.append(jth)
                self.gridSystem.removed.append(ith)
                self.gridSystem.getPlayerIndex()

        def evaluateStep(self):
                self.accelerateCuda()
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
                self.accelerateCuda()
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
                        grav_mag = 0
                        self.collisionDetected(player, names, mass, pos,
                                               vel, acc, rad, ith, jth)

        def accelerateCuda(self):
                G=2.93558*10**-4
                epsilon = 0.01
                for i in range(0,self.gridSystem.count):
                        if(self.gridSystem.names[i] != 'DELETED'):
                                for j in range(0,i):
                                        if(self.gridSystem.names[j] != 'DELETED'):
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
                        if self.gridSystem.names[i]=="DELETED":
                                self.gridSystem.removeBody(i)
                self.gridSystem.collisions = []

        def calVelPosCuda(self):
                for i in range(0,self.gridSystem.count):
                        self.gridSystem.vel[i][0]+=self.dt*self.gridSystem.acc[i][0]
                        self.gridSystem.vel[i][1]+=self.dt*self.gridSystem.acc[i][1]
                        self.gridSystem.vel[i][2]+=self.dt*self.gridSystem.acc[i][2]

                        self.gridSystem.pos[i][0]+=self.dt*self.gridSystem.vel[i][0]
                        self.gridSystem.pos[i][1]+=self.dt*self.gridSystem.vel[i][1]
                        self.gridSystem.pos[i][2]+=self.dt*self.gridSystem.vel[i][2]
