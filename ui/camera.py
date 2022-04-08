import numpy as np
from data_structure.math import *
from utility.transform import Rotation
from OpenGL.GLU import *

class Camera:
    def __init__(self, pos=Vector3(0.,1.,5.), lookat=Vector3(0.,0.,0.)):
        self.pos = pos
        self.lookat = lookat

