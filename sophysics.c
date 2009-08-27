#include <stdio.h>
#include <math.h>
#include <stdbool.h>

float G =0.000293558;
epsilon = 0.01;
void accGravSingle(float* mass, float* pos[3], float* vel[3], float* acc[3], float* rad, int ith, int jth)
{

                float d_x = *(pos+jth)[0] - *(pos+ith)[0];
                float d_y = *(pos+jth)[1] - *(pos+ith)[1];
                float d_z = *(pos+jth)[2] - *(pos+ith)[2];
                float radius = d_x*d_x + d_y*d_y + d_z*d_z;
                float rad2 =sqrt(radius);
                float grav_mag = 0.0;
                
                if (rad2 > rad[ith]+rad[jth])
		{
                        grav_mag = G/pow((radius+epsilon),(3.0/2.0));
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

                
void calVelPos(float* mass, float* pos[3], float* vel[3], float* acc[3], float* rad, int count, float dt)
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

void accelerateAll(float* mass, float* pos[3], float* vel[3], float* acc[3], float* rad, int count, float dt)
{
	int i =0;
	int j =0;
	for (i=0; i<count;i++)
		{
		for (j=0; j<i;j++)
			{
			 accGravSingle(mass, pos, vel, acc, rad, i, j);
			}
		}
calVelPos(mass, pos, vel, acc, rad, count, dt);
}
