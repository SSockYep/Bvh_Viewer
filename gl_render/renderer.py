import pdb
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

import glfw
from scipy.fftpack import sc_diff

from data_structure.bvh_tree import BvhTree, Node
from data_structure.animation import Pose
from data_structure.math import *
from utility.transform import Rotation, Translation, Transform
from .camera import Camera


class Renderer:
    def __init__(self, scale=0.01):
        self.scale = scale

    def clear(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glLoadIdentity()
        glScalef(self.scale, self.scale, self.scale)

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

    def render_line(self, start, end, color):
        glBegin(GL_LINES)
        glColor3ubv(color)
        glVertex3fv(start.to_numpy())
        glVertex3fv(end.to_numpy())
        glEnd()

    def render_pose(
        self, skeleton, pose, color=np.array([255, 255, 255], dtype=np.ubyte)
    ):
        root = skeleton.root
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()

        def dfs(node):
            idx = skeleton.get_index_of_node(node)
            rotation = pose.rotations[idx]
            offset = node.offset
            translation = Translation(offset)
            glPushMatrix()
            if node.is_root():
                root_origin = node.offset
                root_translation = pose.root_translation
                glMultTransposeMatrixf(root_translation.to_matrix().to_numpy())
                # glMultTransposeMatrixf(translation.to_matrix().to_numpy())
                glMultTransposeMatrixf(rotation.to_matrix().to_numpy())

            else:
                self.render_line(Vector3(0, 0, 0), offset, color)
                glMultTransposeMatrixf(translation.to_matrix().to_numpy())
                glMultTransposeMatrixf(rotation.to_matrix().to_numpy())
            if node.is_leaf():
                self.render_line(Vector3(0, 0, 0), node.end, color)
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
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(1.0, 0.0, 0.0)
        glColor3ub(0, 255, 0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 1.0, 0.0)
        glColor3ub(0, 0, 255)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, 1.0)
        glEnd()

        for i in range(-20, 20):
            for j in range(-20, 20):
                glBegin(GL_QUADS)
                if (i + j) % 2 == 0:
                    glColor3ub(30, 30, 30)
                else:
                    glColor3ub(120, 120, 120)
                glVertex3f(i * 0.2, 0, j * 0.2)
                glVertex3f((i + 1) * 0.2, 0, j * 0.2)
                glVertex3f((i + 1) * 0.2, 0, (j + 1) * 0.2)
                glVertex3f(i * 0.2, 0, (j + 1) * 0.2)
                glEnd()
        glScalef(self.scale, self.scale, self.scale)

    def render_point(self, pos):
        glMatrixMode(GL_MODELVIEW)
        glPointSize(7)
        glColor3ub(0, 255, 255)
        glBegin(GL_POINTS)
        glVertex(pos.x, pos.y, pos.z)
        glEnd()
