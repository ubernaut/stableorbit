#include <stdio.h>
#include <math.h>
#include <stdbool.h>
/*
typedef struct cSystem {
  int N;
  int count = 50;
  int player=0;
  char* names = [""];
  float mass= [0.0];
  float rad = [0.0];
  float pos = [[0.0,0.0,0.0]];
  float ori = [[0.0,0.0,0.0]];
  float vel = [[0.0,0.0,0.0]];
  float acc = [[0.0,0.0,0.0]];
  float allocated =1;
 
} System;
*/
void accGravSingle(float* mass, float* pos[3], float* vel[3], float* acc[3], float* rad, int ith, int jth)
{
//                float d_x = *(pos+jth)[0] - *(pos+ith)[0];

                float d_x = *(pos+jth)[0] - *(pos+ith)[0];
                float d_y = *(pos+jth)[1] - *(pos+ith)[1];
                float d_z = *(pos+jth)[2] - *(pos+ith)[2];
                float radius = d_x*d_x + d_y*d_y + d_z*d_z;
                float rad2 =sqrt(radius);
                float grav_mag = 0.0;
                
                if (rad2 > rad[ith]+rad[jth])
		{
                        grav_mag = G/((radius+epsilon)**(3.0/2.0))
		}
                else
		{
                        //print "collision i ",ith," j ",jth
                        //print rad2
                        grav_mag = 0
                }
              
                grav_x=grav_mag*d_x
                grav_y=grav_mag*d_y
                grav_z=grav_mag*d_z
                   
                acc[ith][0] +=grav_x*mass[jth]
                acc[ith][1] +=grav_y*mass[jth]
                acc[ith][2] +=grav_z*mass[jth]
                
                *(acc+jth)[0] +=grav_x*mass[ith]
                *(acc+jth)[1] +=grav_y*mass[ith]
                *(acc+jth)[2] +=grav_z*mass[ith]   
}

bool  starting;

void update_position(System* p_system, double dt)
{
  int i;
  for (i=0;i<p_system->N;i++)
  {
    p_system->bodies[i].position.x += p_system->bodies[i].velocity.x*dt;
    p_system->bodies[i].position.y += p_system->bodies[i].velocity.y*dt;
    p_system->bodies[i].position.z += p_system->bodies[i].velocity.z*dt;
  }
}

void update_velocity(System* p_system, float dt)
{
  int i;
  for (i=0;i<p_system->N;i++)
  {
    p_system->bodies[i].velocity.x += p_system->bodies[i].acceleration.x*dt;
    p_system->bodies[i].velocity.y += p_system->bodies[i].acceleration.y*dt;
    p_system->bodies[i].velocity.z += p_system->bodies[i].acceleration.z*dt;
    
    p_system->bodies[i].acceleration.x = 0.0;
    p_system->bodies[i].acceleration.y = 0.0;
    p_system->bodies[i].acceleration.z = 0.0;
  }
}
/*
void accelerate(System* p_system)
{
  int i, j;
  float dx, dy, dz;
  float G=0.000323558;
  float epsilon=0.01;
  float grav_x, grav_y, grav_z, grav_mag, dist_squared;
  for (i=0;i<p_system->N;i++) 
  {
    for(j=0;j<i;j++) 
    {
      dx = p_system->bodies[j].position.x - p_system->bodies[i].position.x;
      dy = p_system->bodies[j].position.y - p_system->bodies[i].position.y;
      dz = p_system->bodies[j].position.z - p_system->bodies[i].position.z;
      dist_squared = dx*dx + dy*dy + dz*dz;
      
      grav_mag = G/pow((dist_squared+epsilon),(3.0/2.0));
      
      grav_x=grav_mag*dx;
      grav_y=grav_mag*dy;
      grav_z=grav_mag*dz;

      p_system->bodies[i].acceleration.x += grav_x*p_system->bodies[j].mass;
      p_system->bodies[j].acceleration.x -= grav_x*p_system->bodies[i].mass;
      
      p_system->bodies[i].acceleration.y += grav_y*p_system->bodies[j].mass;
      p_system->bodies[j].acceleration.y -= grav_y*p_system->bodies[i].mass;
      
      p_system->bodies[i].acceleration.z += grav_z*p_system->bodies[j].mass;
      p_system->bodies[j].acceleration.z -= grav_z*p_system->bodies[i].mass;
    }
  }
}

void do_step(System* p_system, float dt)
{
  int i, j;
  for(j=0;j<p_system->N;j++)
  {
    accelerate(p_system);
    if (starting)
      update_velocity(p_system, dt/2.0);
    else 
      update_velocity(p_system, dt);
    update_position(p_system, dt);
  }
}
*/
