import pycuda.autoinit
import pycuda.driver as drv
import numpy
from numpy import ndarray

mod = drv.SourceModule("""


__global__ void doubler(float *pos)
{
    int idx = threadIdx.x+ threadIdx.y*3;

    pos[idx] *= 2;
}
__global__ void getdeltas(float** dest, float** ithpos, float** jthpos)
//__global__ void getdeltas(float* dest[3], float* ithpos[3], float* jthpos[3])
{
    //float tempdest[3]={0,0,0}

    int idx = threadIdx.x;
    *(dest)[0] = *(jthpos)[0] - *(ithpos)[0];
    *(dest)[1] = *(jthpos)[1] - *(ithpos)[1];
    *(dest)[2] = *(jthpos)[2] - *(ithpos)[2];
}

__global__ void accGravSingle(float* mass, float* pos[3], float* vel[3], float* acc[3], float* rad, int ith, int jth)
{
                float G =0.000293558; 
                float epsilon = 0.01;
                float d_x = *(pos+jth)[0] - *(pos+ith)[0];
                float d_y = *(pos+jth)[1] - *(pos+ith)[1];
                float d_z = *(pos+jth)[2] - *(pos+ith)[2];
                float radius = d_x*d_x + d_y*d_y + d_z*d_z;
                float rad2 = sqrt(radius);
                float grav_mag = 0.0;

                if (rad2 > *(rad+ith)+ *(rad+jth))
		{
                    grav_mag =G/pow(radius+epsilon,3/2);
		}
                else
		{
                        grav_mag = 0;
                }
              
                float grav_x=grav_mag*d_x;
                float grav_y=grav_mag*d_y;
                float grav_z=grav_mag*d_z;
                   
                *(acc+ith)[0] +=grav_x*mass[jth];
                *(acc+ith)[1] +=grav_y*mass[jth];
                *(acc+ith)[2] +=grav_z*mass[jth];
                
                *(acc+jth)[0] +=grav_x*mass[ith];
                *(acc+jth)[1] +=grav_y*mass[ith];
                *(acc+jth)[2] +=grav_z*mass[ith];   
}


                
__global__ void calVelPos(float* mass, float* pos[3], float* vel[3], float* acc[3], float* rad, int count, float dt)
{
	int i;
	for (i=0; i<count;i++)
		{
                *(vel+i)[0]+=dt* *(acc+i)[0];
                *(vel+i)[2]+=dt* *(acc+i)[1];
                *(vel+i)[1]+=dt* *(acc+i)[2];

                *(pos+i)[0]+=dt* *(vel+i)[0];
                *(pos+i)[2]+=dt* *(vel+i)[1];
                *(pos+i)[1]+=dt* *(vel+i)[2];

		*(acc+i)[0]=0;
		*(acc+i)[1]=0;
		*(acc+i)[2]=0;
		}
}

__global__ void oncePerBody(float* mass, float* pos[3], float* vel[3], float* acc[3], float* rad, int count, float dt, float i)
{
    const int xthread = threadIdx.x;
    
    int j =0;
    for (j=0; j<i;j++)
    {
    //initrd.imgaccGravSingle(mass, pos, vel, acc, rad, i, j);
    }

}
__global__ void accelerateAll(float* mass, float* pos[3], float* vel[3], float* acc[3], float* rad, int count, float dt)
{
	int i =0;
	for (i=0; i<count;i++)
		{
		 //initrd.imgaccGravSingle(mass, pos, vel, acc, rad, i, j);
		}
//calVelPos(mass, pos, vel, acc, rad, count, dt);
}
""")

getdeltas = mod.get_function("getdeltas")
doubler = mod.get_function("doubler")
posi = ndarray([3,3], numpy.float32)
posj = ndarray([3,1], numpy.float32)
posd = ndarray([3,1], numpy.float32)
posi[0][0]=6
posi[0][1]=6
posi[0][2]=6
posi[1][0]=6
posi[1][1]=6
posi[1][2]=6
posi[2][0]=6
posi[2][1]=6
posi[2][2]=6
posj[0]=3
posj[1]=3
posj[2]=3
posd[0]=0
posd[1]=0
posd[2]=0

print "shape",posi.shape
print posi
#posj = array([0.0,0.0,0.0]).astype(numpy.float32)
#dest = array([(0.0,0.0,0.0)]).astype(numpy.float32)
allgpu = pycuda.driver.mem_alloc(posi.nbytes)#+posj.nbytes+posd.nbytes)
pycuda.driver.memcpy_htod(allgpu, posi)
doubler(posi, block = (3,3,1))
print posi
#getdeltas(drv.Out(posd), drv.In(posi), drv.In(posj),block = (1,1,1))
#a = numpy.random.randn(400).astype(numpy.float32)
#print a
#b = numpy.random.randn(400).astype(numpy.float32)
#print b
#dest = numpy.zeros_like(a)
#multiply_them(
#        drv.Out(dest), drv.In(a), drv.In(b),
#        block=(400,1,1))
#

#print dest
#print dest-a*b
