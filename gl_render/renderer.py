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
            translation = Translation(offset)
            glPushMatrix()
            if node.is_root():
                root_origin = node.offset
                root_translation = pose.root_translation
                # glMultTransposeMatrixf(translation.to_matrix().to_numpy())
                glMultTransposeMatrixf(root_translation.to_matrix().to_numpy())
                glMultTransposeMatrixf(rotation.to_matrix().to_numpy())

            else:
                self.render_line(Vector3(0, 0, 0), offset)
                glMultTransposeMatrixf(translation.to_matrix().to_numpy())
                glMultTransposeMatrixf(rotation.to_matrix().to_numpy())
            if node.is_leaf():
                self.render_line(Vector3(0, 0, 0), node.end)
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
        node = skeleton.get_node_by_name(node_name)
        pos = self._get_node_global_position(skeleton, node, pose)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glScale(scale, scale, scale)
        glPointSize(7)
        glColor3ub(0, 255, 255)
        glBegin(GL_POINTS)
        glVertex(pos.x, pos.y, pos.z)
        glEnd()

    def render_joint_velocity(
        self, node_name, skeleton, animation, pose_idx, scale=0.01
    ):
        if pose_idx <= 0 or pose_idx >= len(animation.poses):
            raise ValueError
        node = skeleton.get_node_by_name(node_name)
        pose_now = animation.get_pose(pose_idx)
        pose_prev = animation.get_pose(pose_idx - 1)
        position_now = self._get_node_global_position(skeleton, node, pose_now)
        position_prev = self._get_node_global_position(skeleton, node, pose_prev)

        velocity = position_now + (
            (position_now - position_prev) / animation.frame_time
        )
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glScale(scale, scale, scale)
        glColor3ub(255, 255, 0)
        glBegin(GL_LINES)
        glVertex(position_now.x, position_now.y, position_now.z)
        glVertex(velocity.x, velocity.y, velocity.z)
        glEnd()

    def _get_node_global_position(self, skeleton, node, pose):
        mat = Matrix4x4(np.eye(4, 4))
        idx = skeleton.get_index_of_node(node)
        while True:
            if node.is_root():
                mat = (
                    pose.root_translation.to_matrix()
                    # @ Translation(node.offset).to_matrix()
                    @ pose.rotations[idx].to_matrix()
                    @ mat
                )
                break
            mat = (
                Translation(node.offset).to_matrix()
                @ pose.rotations[idx].to_matrix()
                @ mat
            )
            node = node.parent
            idx = skeleton.get_index_of_node(node)
        pos = mat @ Vector3(0, 0, 0)
        return pos
