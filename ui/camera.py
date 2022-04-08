import numpy as np
from data_structure.math import *
from utility.transform import Rotation
from OpenGL.GLU import *

class Camera:
    def __init__(self, pos=Vector3(0,1,5), lookat=Vector3(0,0,0)):
        self.pos = pos
        self.lookat = lookat

    def render_perspective(self):
        gluPerspective(45,1,1,10)
        gluLookAt(self.pos.x, self.pos.y, self.pos.z,
                self.lookat.x, self.lookat.y, self.lookat.z, 0, 1, 0)