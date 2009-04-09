from ctypes import *

class Point(Structure):
  _fields_ = ( "x", c_float), ( "y", c_float), ( "z", c_float)

class Body(Structure):
  _fields_ = ( "mass", c_float), ( "position", Point), ("velocity", Point), ("acceleration", Point)

class System(Structure):
  _fields_ = ("N", c_int), ("bodies", Body*60)