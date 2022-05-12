import pytest
import numpy as np
from utility.bvh_loader import BvhLoader
from utility.transform import Rotation, Transform, Translation
from data_structure.bvh_tree import Node
from data_structure.math import *


class TestTranslation:
    def test_from_vector(self):
        assert Translation.from_vector(Vector3(1, 2, 3)).vec == Vector3(1, 2, 3)

    def test_from_mat(self):
        mat = np.eye(4)
        mat[:, 3] = [1, 2, 3, 1]
        assert Translation.from_matrix(mat).vec == Vector3(1, 2, 3)

    def test_to_vector(self):
        assert Translation(Vector3(12, 3, 4)).to_vector() == Vector3(12, 3, 4)

    def test_to_mat(self):
        mat = np.eye(4)
        mat[:, 3] = [1, 2, 3, 1]
        assert Translation(Vector3(1, 2, 3)).to_matrix() == Matrix4x4(mat)

    def test_eq(self):
        assert Translation(Vector3(1, 2, 3)) == Translation(Vector3(1, 2, 3))


class TestRotation:
    def test_equality(self):
        left = Rotation()
        right = Rotation()
        assert left == right

    def test_from_euler(self):
        assert Rotation.from_euler(
            "xyz", np.pi / 6, np.pi / 4, np.pi / 3
        ).quaternion == Quaternion(0.82236317, 0.02226003, 0.43967974, 0.36042341)

    def test_from_matrix(self):
        # matrix and quaternion for rotate pi/6, pi/4, pi/3 (euler xyz)
        test_mat = np.array(
            [
                [0.35355339, -0.5732233, 0.73919892, 0.0],
                [0.61237244, 0.73919892, 0.28033009, 0.0],
                [-0.70710678, 0.35355339, 0.61237244, 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ]
        )
        assert Rotation.from_matrix(test_mat) == Rotation(
            Quaternion(0.82236317, 0.02226003, 0.43967974, 0.36042341)
        )

    def test_to_matrix(self):
        quater = Quaternion(np.cos(np.pi / 3), np.sin(np.pi / 3), 0, 0)
        r = Rotation(quater)  # cos(1/3*pi), sin(1/3*pi), 0, 0
        test_nparr = np.array(
            [
                [1, 0, 0, 0],
                [0, np.cos(np.pi * 2 / 3), -np.sin(np.pi * 2 / 3), 0],
                [0, np.sin(np.pi * 2 / 3), np.cos(np.pi * 2 / 3), 0],
                [0, 0, 0, 1],
            ]
        )
        test_mat = Matrix4x4(test_nparr)
        assert r.to_matrix() == test_mat

    def test_rotate(self):
        point = Vector3(0, 0, 1)
        rotation = Rotation.from_euler("xyz", 0, np.pi, 0)
        assert rotation.rotate(point) == Vector3(0, 0, -1)

    def test_eq(self):
        assert Rotation(Quaternion(1, 0, 0, 0)) == Rotation(Quaternion(-1, 0, 0, 0))

    def test_to_vec(self):
        assert Rotation(Quaternion(1, 0, 0, 0)).to_vec() == Vector3(0, 0, 0)

    def test_mult_scalar(self):
        assert Rotation.from_euler("xyz", np.pi / 3, 0, 0) * 0.5 == Rotation.from_euler(
            "xyz", np.pi / 6, 0, 0
        )


class TestTransform:
    def test_init(self):
        assert Transform()

    def test_to_matrix(self):
        t = Translation.from_vector(Vector3(1, 1, 1))
        r = Rotation.from_euler("xyz", np.pi / 2, 0, 0)
        np_mat = np.array(
            [[1, 0, 0, 1], [0, 0, -1, 1], [0, 1, 0, 1], [0, 0, 0, 1]], dtype=np.float64
        )
        assert Transform(t, r).to_matrix() == Matrix4x4(np_mat)


class TestLoader:
    def test_init(self):
        loader = BvhLoader(filename="test.bvh")
        assert loader.filename == "test.bvh"
