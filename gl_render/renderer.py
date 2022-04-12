import pdb
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

import glfw

from data_structure.bvh_tree import BvhTree, Node
from data_structure.animation import Pose
from data_structure.math import *
from utility.transform import Rotation, Translation, Transform
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
        glBegin(GL_LINES)
        glColor3ub(255, 255, 255)
        glVertex3fv(start.to_numpy())
        glVertex3fv(end.to_numpy())
        glEnd()

    def render_pose(self, skeleton, pose, scale=0.01):
        root = skeleton.root

        glPointSize(5)
        glColor3ub(255, 255, 255)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glScalef(scale, scale, scale)
        glPushMatrix()

        def dfs(node):
            idx = skeleton.get_index_of_node(node)
            rotation = pose.rotations[idx]
            offset = node.offset
            if node.is_root():
                root_translation = pose.root_translation
                glMultTransposeMatrixd(root_translation.to_matrix().to_numpy())
            translation = Translation(node.offset)
            # pdb.set_trace()
            glMultTransposeMatrixf(rotation.to_matrix().to_numpy())
            if not (node.is_root()):
                start = Vector3(0, 0, 0)
                end = offset
                self.render_line(start, end)
            glMultTransposeMatrixf(translation.to_matrix().to_numpy())
            glPushMatrix()
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

    def render_joint_pos(self, node_name, skeleton, pose, scale=0.01):
        mat = Matrix4x4(np.eye(4, 4))
        node = skeleton.get_node_by_name(node_name)
        idx = skeleton.get_index_of_node(node)
        while True:
            mat = (
                pose.rotations[idx].to_matrix()
                @ Translation(node.offset).to_matrix()
                @ mat
            )
            if node.is_root():
                mat = pose.root_translation.to_matrix() @ mat
                break
            node = node.parent
            idx = skeleton.get_index_of_node(node)
        pos = mat @ Vector3(0, 0, 0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glScale(scale, scale, scale)

        glPointSize(5)
        glBegin(GL_POINTS)
        glVertex(pos.x, pos.y, pos.z)
        glEnd()
