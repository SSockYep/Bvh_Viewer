from data_structure.math import *
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

class Renderer:
    def __init__(self):
        pass

    def clear(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        # glPolygonMode(GL_FRONT_AND_BACK, GL_LINES)

    def render_line(self, start, end):
        glBegin(GL_LINES)
        glVertex3fv(start.to_numpy())
        glVertex3fv(end.to_numpy())
        glEnd()
        return True
    
    def render_axis(self):
        glBegin(GL_LINES)
        glColor3ub(255,0,0)
        glVertex3fv(np.array([0.,0.,0.]))
        glVertex3fv(np.array([1.,0.,0.]))
        glColor3ub(0,255,0)
        glVertex3fv(np.array([0.,0.,0.]))
        glVertex3fv(np.array([0.,1.,0.]))
        glColor3ub(0,0,255)
        glVertex3fv(np.array([0.,0.,0.]))
        glVertex3fv(np.array([0.,0.,1.]))
        glEnd()