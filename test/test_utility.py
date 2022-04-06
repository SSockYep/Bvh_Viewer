import pytest
import numpy as np
from utility.transform import Rotation
from utility.bvh_tree import Node
from data_structure.math import *

class TestRotation:
    def test_equality(self):
        left = Rotation()
        right = Rotation()
        assert left == right

    def test_from_euler(self):
        assert Rotation.from_euler('xyz', np.pi/6, np.pi/4, np.pi/3).quaternion == Quaternion(0.82236317, 0.02226003, 0.43967974, 0.36042341)

    def test_from_matrix(self):
        # matrix and quaternion for rotate pi/6, pi/4, pi/3 (euler xyz)
        test_mat = np.array([[ 0.35355339, -0.5732233 ,  0.73919892, 0.],
                             [ 0.61237244,  0.73919892,  0.28033009, 0.],
                             [-0.70710678,  0.35355339,  0.61237244, 0.],
                             [0., 0., 0., 1.]])
        assert Rotation.from_matrix(test_mat) == Rotation(Quaternion(0.82236317, 0.02226003, 0.43967974, 0.36042341))

    def test_to_matrix(self):
        quater = Quaternion(np.cos(np.pi/3), np.sin(np.pi/3), 0, 0)
        r = Rotation(quater) # cos(1/3*pi), sin(1/3*pi), 0, 0
        test_nparr = np.array([[1, 0, 0, 0],
                                [0, np.cos(np.pi*2/3), -np.sin(np.pi*2/3), 0],
                                [0, np.sin(np.pi*2/3), np.cos(np.pi*2/3), 0],
                                [0, 0, 0, 1]])
        test_mat = Matrix4x4(test_nparr)
        assert r.to_matrix() == test_mat

    def test_rotate(self):
        point = Vector3(0,0,1)
        rotation = Rotation.from_euler('xyz', 0, np.pi, 0)
        assert rotation.rotate(point) == Vector3(0,0,-1)

class TestNode:
    def test_node_initialize(self):
        assert Node() != None

    def test_offset(self):
        node = Node()
        node.offset = Vector3(1,1,1)
        assert node.offset == Vector3(1,1,1)

    def test_set_offset_on_init(self):
        node = Node(Vector3(1,1,1))
        assert node.offset == Vector3(1,1,1)

    def test_set_node_name(self):
        node = Node()
        node.set_name("test_name")
        assert node.get_name() == "test_name"