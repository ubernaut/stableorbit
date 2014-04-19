#! /usr/bin/python
import pycuda.gpuarray as gpuarray
import pycuda.driver as cuda
import pycuda.autoinit
import numpy
from pycuda.curandom import rand as curand

N=1000000
pos = numpy.random.randn(N,4)
pos = pos.astype(numpy.float32)
vel = numpy.random.randn(N,4)
vel = vel.astype(numpy.float32)


cu_code="""
__global__ void integrate(float4* position, 
                          float4* velocity,
                          uint N)
{
  int idx = blockIdx.x * blockDim.x + threadIdx.x;
  float4 pos = position[idx];
  for(int i = 0; i < N; ++i)
  {
    position[idx].x = 0;
    pos.x = 0.0;
  }
  
}
"""


mod = cuda.SourceModule(cu_code)
integrate = mod.get_function("integrate")
integrate(cuda.InOut(pos),cuda.InOut(vel),block=(100,1,1),grid=(10000,1))

print pos
