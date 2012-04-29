__kernel void part2(__global float4* pos, __global float4* color, __global float4* vel, __global float4* pos_gen, __global float4* vel_gen, __local float4* pos_shared, float dt, unsigned int num)
{
    //get our index in the array
    unsigned int i = get_global_id(0);
    unsigned int tid = get_local_id(0);
    unsigned int block_dim = get_local_size(0);

    //copy position and velocity for this iteration to a local variable
    //note: if we were doing many more calculations we would want to have opencl
    //copy to a local memory array to speed up memory access (this will be the subject of a later tutorial)
    float4 p = pos[i];
    float4 v = vel[i];

    ////we've stored the life in the fourth component of our velocity array
    //float life = vel[i].w;
    ////decrease the life by the time step (this value could be adjusted to lengthen or shorten particle life
    //life -= dt;
    ////if the life is 0 or less we reset the particle's values back to the original values and set life to 1
    //if(life <= 0.f)
    //{
    //    p = pos_gen[i];
    //    v = vel_gen[i];
    //    life = 1.0f;    
    //}

    float4 acc = (float4) (0.0f, 0.0f, 0.0f, 0.0f);

    int tile=0;
    int body, j;
    for (body=0; body <num; body += block_dim, tile++)
    {
        pos_shared[tid] = pos_gen[tile * block_dim + tid];
        barrier(CLK_LOCAL_MEM_FENCE);
        for (j=0; j < block_dim; j++)
        {
            float4 pj = pos_shared[j];
            float4 r =  pj - p;
            float dist = sqrt(r.x * r.x + r.y * r.y + r.z * r.z);
            dist += 0.1;
            float inv_dist = 1.0f / (dist);
            float inv_dist_cubed = inv_dist * inv_dist * inv_dist;
            float s = pj.w * inv_dist_cubed;
            acc -= r * s;
        }
        barrier(CLK_LOCAL_MEM_FENCE);
    }

    v -= acc * dt;
    p.x += v.x*dt;
    p.y += v.y*dt;
    p.z += v.z*dt;

    //store the updated life in the velocity array
    //v.w = life;

    //update the arrays with our newly computed values
    pos[i] = p;
    vel[i] = v;

    //you can manipulate the color based on properties of the system
    //here we adjust the alpha
    //color[i].w = life;

}
