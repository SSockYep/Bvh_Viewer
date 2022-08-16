import pdb
from unittest import result
import numpy as np
from copy import copy
from data_structure.math import *


class Translation:
    def __init__(self, v: Vector3 = Vector3()):
        self.vec = copy(v)

    def __eq__(self, other):
        if not isinstance(other, Translation):
            raise TypeError
        return self.vec == other.vec

    def __ne__(self, other):
        if self.__eq__(other):
            return False
        return True

    def __add__(self, other):
        if isinstance(other, Vector3):
            return Translation.from_vector(self.vec + other)
        if isinstance(other, Translation):
            return Translation.from_vector(self.vec + other.vec)
        raise TypeError

    def __sub__(self, other):
        if isinstance(other, Vector3):
            return Translation.from_vector(self.vec - other)
        if isinstance(other, Translation):
            return Translation.from_vector(self.vec - other.vec)
        raise TypeError

    def __mul__(self, other):
        if not isinstance(other, float):
            raise TypeError
        return Translation.from_vector(self.vec * other)

    @classmethod
    def from_vector(cls, v: Vector3):
        return cls(v)

    @classmethod
    def from_matrix(cls, m: Matrix4x4):
        v = Vector3(m[0, 3], m[1, 3], m[2, 3])
        return cls(v)

    def to_vector(self):
        return copy(self.vec)

    def to_matrix(self):
        mat = np.eye(4)
        mat[:3, 3] = self.vec.to_numpy()
        return Matrix4x4(mat)


class Rotation:
    def __init__(self, q: Quaternion = Quaternion()):
        if not np.isclose(q @ q, 1):
            raise ValueError
        self.quaternion = copy(q)

    def __eq__(self, other):
        if not isinstance(other, Rotation):
            raise TypeError
        return (
            self.quaternion == other.quaternion or self.quaternion == -other.quaternion
        )

    def __ne__(self, other):
        if self.__eq__(other):
            return False
        return True

    def __add__(self, other):
        if isinstance(other, Quaternion):
            return Rotation.from_quaternion(self.quaternion * other)
        if isinstance(other, Rotation):
            return Rotation.from_quaternion(self.quaternion * other.quaternion)
        raise TypeError

    def __sub__(self, other):
        if isinstance(other, Quaternion):
            return Rotation.from_quaternion(other.inv() * self.quaternion)
        if isinstance(other, Rotation):
            return Rotation.from_quaternion(other.quaternion.inv() * self.quaternion)
        raise TypeError

    def __mul__(self, other):
        if not isinstance(other, float):
            raise TypeError
        if np.isclose(other, 0):
            return Rotation(Quaternion(1, 0, 0, 0))
        return Rotation.from_vec(self.to_vec() * other)

    @classmethod
    def from_quaternion(cls, q: Quaternion):
        return cls(q)

    @classmethod
    def from_matrix(cls, mat: Matrix4x4):
        if not np.allclose(mat[:, 3], [0, 0, 0, 1]):
            raise ValueError
        tr = np.array(
            [mat[0, 0], mat[1, 1], mat[2, 2], mat[0, 0] + mat[1, 1] + mat[2, 2]]
        )
        arg_max = tr.argmax()
        if arg_max == 3:
            w4 = np.sqrt(tr[3] + 1) * 2
            w = w4 / 4
            x = (mat[2, 1] - mat[1, 2]) / w4
            y = (mat[0, 2] - mat[2, 0]) / w4
            z = (mat[1, 0] - mat[0, 1]) / w4
        elif arg_max == 0:
            x4 = np.sqrt(1 + tr[0] - tr[1] - tr[2])
            w = (mat[2, 1] - mat[1, 2]) / x4
            x = w4 / 4
            y = (mat[0, 1] + mat[1, 0]) / x4
            z = (mat[0, 2] + mat[2, 0]) / x4
        elif arg_max == 1:
            y4 = np.sqrt(1 + tr[1] - tr[2] - tr[0])
            w = (mat[0, 2] - mat[2, 0]) / y4
            x = (mat[0, 1] + mat[1, 0]) / y4
            y = y4 / 4
            z = (mat[1, 2] + mat[2, 1]) / y4
        else:
            z4 = np.sqrt(1 + tr[2] - tr[0] - tr[1])
            w = (mat[1, 0] - mat[0, 1]) / z4
            x = (mat[0, 2] + mat[2, 0]) / z4
            y = (mat[1, 2] + mat[2, 1]) / z4
            z = z4 / 4
        if not np.isclose(np.array([w, x, y, z]) @ np.array([w, x, y, z]), 1):
            raise ValueError
        return cls(Quaternion(w, x, y, z))

    @classmethod
    def from_euler(cls, seq: str = "xyz", *angles):
        if len(seq) != 3 or len(angles) != 3:
            raise ValueError
        if seq[0] == seq[1] or seq[1] == seq[2]:
            raise ValueError
        if seq[0] not in "xyz" or seq[1] not in "xyz" or seq[2] not in "xyz":
            raise ValueError

        def rotate(axis, angle):
            params = [np.cos(angle / 2), 0, 0, 0]
            i = int()
            if str.lower(axis) == "x":
                i = 1
            elif str.lower(axis) == "y":
                i = 2
            elif str.lower(axis) == "z":
                i = 3
            else:
                raise ValueError
            params[i] = np.sin(angle / 2)
            return Quaternion(params[0], params[1], params[2], params[3])

        q = []
        for i in range(3):
            q.append(rotate(seq[i], angles[i]))
        return cls(q[2] * q[1] * q[0])

    @classmethod
    def from_vec(cls, vec: Vector3):
        angle = vec.magnitude()
        if np.isclose(angle, 0):
            return cls()
        w = np.cos(angle / 2)
        v = (vec / vec.magnitude()) * np.sin(angle / 2)
        return cls(Quaternion(w, v.x, v.y, v.z))

    def to_quaternion(self):
        return copy(self.quaternion)

    def to_vec(self):
        theta = np.arccos(self.quaternion.w)
        if np.isclose(theta, 0):
            return Vector3(0, 0, 0)
        if np.isclose(theta, np.pi):
            x = self.quaternion.x
            y = self.quaternion.y
            z = self.quaternion.z
        else:
            x = self.quaternion.x / np.sin(theta)
            y = self.quaternion.y / np.sin(theta)
            z = self.quaternion.z / np.sin(theta)
        vec = Vector3(x, y, z)
        if np.isclose(vec.magnitude(), 0):
            return Vector3(0, 0, 0)
        vec = (vec / vec.magnitude()) * 2 * theta
        return vec

    def to_matrix(self):
        q = self.quaternion
        row0 = np.array(
            [
                1 - 2 * q.y * q.y - 2 * q.z * q.z,
                2 * q.x * q.y - 2 * q.z * q.w,
                2 * q.x * q.z + 2 * q.y * q.w,
                0,
            ]
        )
        row1 = np.array(
            [
                2 * q.x * q.y + 2 * q.z * q.w,
                1 - 2 * q.x * q.x - 2 * q.z * q.z,
                2 * q.y * q.z - 2 * q.x * q.w,
                0,
            ]
        )
        row2 = np.array(
            [
                2 * q.x * q.z - 2 * q.y * q.w,
                2 * q.y * q.z + 2 * q.x * q.w,
                1 - 2 * q.x * q.x - 2 * q.y * q.y,
                0,
            ]
        )
        row3 = np.array([0, 0, 0, 1])
        return Matrix4x4(np.array([row0, row1, row2, row3]))

    def rotate(self, point: Vector3) -> Vector3:
        q = self.quaternion
        q_conj = q.conjugate()
        p = Quaternion(0, point.x, point.y, point.z)
        rotated = q * p * q_conj
        return Vector3(rotated.x, rotated.y, rotated.z)


class Transform:
    def __init__(self, trans: Translation = Translation(), rot: Rotation = Rotation()):
        self.translation = trans
        self.rotation = rot

    def to_matrix(self):
        rot_mat = self.rotation.to_matrix()
        trans_mat = self.translation.to_matrix()
        result_matrix = trans_mat @ rot_mat
        # result_matrix = copy(rot_mat)
        # result_matrix[0, 3] = trans_mat[0, 3]
        # result_matrix[1, 3] = trans_mat[1, 3]
        # result_matrix[2, 3] = trans_mat[2, 3]
        return result_matrix

    def from_matrix(cls, matrix):
        t = Translation.from_matrix(matrix)
        r = Rotation.from_matrix(matrix)
        return cls(t, r)
