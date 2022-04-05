import pytest
import numpy as np
from utility.transform import Rotation
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
