#include <stdio.h>
#include <math.h>

struct Point
{
  float x, y, z;
};

struct Body 
{
  float mass;
  struct Point position, velocity, acceleration;
};

typedef struct System {
  int N;
  struct Body bodies[60];
} System;

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

void accelerate(System* p_system)
{
  int i, j;
  float dx, dy, dz;
  float G=0.000293558;
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
  for(i=0;i<1;i++)
  {
    for(j=0;j<p_system->N;j++)
    {
      accelerate(p_system);
      update_velocity(p_system, dt);
      update_position(p_system, dt);
    }
  }
}
