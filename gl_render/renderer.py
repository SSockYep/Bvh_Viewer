import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

import glfw

from data_structure.animation import Pose
from data_structure.math import *
from .camera import Camera


class Renderer:
    def __init__(self):
        pass

    def clear(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glLoadIdentity()

    def render_perspective(self, cam):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(cam.angle, 1, 1, 100)
        gluLookAt(
            cam.pos.x,
            cam.pos.y,
            cam.pos.z,
            cam.lookat.x,
            cam.lookat.y,
            cam.lookat.z,
            0,
            1,
            0,
        )

    def render_line(self, start, end):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glBegin(GL_LINES)
        glColor3ub(255, 255, 255)
        glVertex3fv(start.to_numpy())
        glVertex3fv(end.to_numpy())
        glEnd()

    def render_pose(self, skeleton, pose, scale=1.0):
        root = skeleton.root

        glPointSize(5)
        glColor3ub(255, 255, 255)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glScalef(scale, scale, scale)
        glPushMatrix()

        def dfs(node):
            idx = skeleton.get_index_of_node(node)
            matrix = pose.transforms[idx].to_matrix().to_numpy()
            glMultTransposeMatrixf(matrix)
            glPushMatrix()
            glBegin(GL_POINTS)
            glVertex3f(0.0, 0.0, 0.0)
            glEnd()

            for child in node.children:
                dfs(child)
            glPopMatrix()

        dfs(root)
        glPopMatrix()

    def render_global_axis(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glBegin(GL_LINES)
        glColor3ub(255, 0, 0)
        glVertex3fv(np.array([0.0, 0.0, 0.0]))
        glVertex3fv(np.array([1.0, 0.0, 0.0]))
        glColor3ub(0, 255, 0)
        glVertex3fv(np.array([0.0, 0.0, 0.0]))
        glVertex3fv(np.array([0.0, 1.0, 0.0]))
        glColor3ub(0, 0, 255)
        glVertex3fv(np.array([0.0, 0.0, 0.0]))
        glVertex3fv(np.array([0.0, 0.0, 1.0]))
        glEnd()
