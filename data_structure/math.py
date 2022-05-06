import numpy as np


class Vector3:
    def __init__(self, x: np.float32 = 0.0, y: np.float32 = 0.0, z: np.float32 = 0.0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "Vector3({}, {}, {})".format(self.x, self.y, self.z)

    def __repr__(self):
        return "Vector3({}, {}, {})".format(self.x, self.y, self.z)

    def __eq__(self, other):
        return (
            np.isclose(self.x, other.x)
            and np.isclose(self.y, other.y)
            and np.isclose(self.z, other.z)
        )

    def __nq__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):  # self + other: Vector addition
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):  # self - other: Vector subtraction
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __truediv__(self, other):  # self / othher: Vector divide by scalar
        return Vector3(self.x / other, self.y / other, self.z / other)

    def __matmul__(self, other):  # self @ other: Vector dot product
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __mul__(self, other):
        if type(other) == Vector3:  # self * other(Vector): Vector cross product
            return Vector3(
                self.y * other.z - self.z * other.y,
                self.z * other.x - self.x * other.z,
                self.x * other.y - self.y * other.x,
            )
        # self * other(scalar): Vector multipy by scalar
        return Vector3(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other):  # self / scalar
        return Vector3(self.x / other, self.y / other, self.z / other)

    @classmethod
    def from_numpy(cls, np_array):
        if type(np_array) != np.ndarray:
            raise ValueError
        if np_array.size != 3 or len(np_array.shape) != 1:
            raise ValueError
        return cls(np_array[0], np_array[1], np_array[2])

    def to_numpy(self, dtype=np.float32):
        return np.array([self.x, self.y, self.z], dtype=dtype)

    def magnitude(self):
        return np.sqrt(self @ self)

    def copy(self):
        return Vector3(self.x, self.y, self.z)

    def dot(self, other):
        return self @ other

    def cross(self, other):
        return self * other


class Quaternion:
    def __init__(
        self, w: np.float32 = 1, x: np.float32 = 0, y: np.float32 = 0, z: np.float32 = 0
    ):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        return (
            np.isclose(self.w, other.w)
            and np.isclose(self.x, other.x)
            and np.isclose(self.y, other.y)
            and np.isclose(self.z, other.z)
        )

    def __str__(self):
        return "Quaternion({}, {}, {}, {})".format(self.w, self.x, self.y, self.z)

    def __repr__(self):
        return "Quaternion({}, {}, {}, {})".format(self.w, self.x, self.y, self.z)

    def __mul__(self, other):
        if isinstance(other, Quaternion):
            a, b, c, d = self.w, self.x, self.y, self.z
            e, f, g, h = other.w, other.x, other.y, other.z
            res = Quaternion(
                (a * e - b * f - c * g - d * h),
                (a * f + b * e + c * h - d * g),
                (a * g - b * h + c * e + d * f),
                (a * h + b * g - c * f + d * e),
            )
            return res
        return Quaternion(
            self.w * other, self.x * other, self.y * other, self.z * other
        )

    def __neg__(self):
        return Quaternion(-self.w, -self.x, -self.y, -self.z)

    def conjugate(self):
        return Quaternion(self.w, -self.x, -self.y, -self.z)


class Matrix4x4:
    def __init__(self, np_array=np.eye(4, 4)):
        if type(np_array) != np.ndarray:
            raise ValueError
        if np_array.shape != (4, 4):
            raise ValueError
        self._mat = np.copy(np_array)

    def __eq__(self, other):
        return np.allclose(self._mat, other._mat)

    def __str__(self):
        return "Matrix4x4: " + self._mat.__str__()

    def __repr__(self):
        return "Matrix4x4: " + self._mat.__str__()

    def __getitem__(self, pair):
        row = pair[0]
        col = pair[1]
        return self._mat[row, col]

    def __add__(self, other):
        if isinstance(other, Matrix4x4):
            return Matrix4x4(self._mat + other._mat)
        elif isinstance(other, Vector3):
            mat = self._mat.copy()
            mat[:3, 3] = other.to_numpy()
            return Matrix4x4(mat)
        raise TypeError

    def __setitem__(self, pair, val):
        row = pair[0]
        col = pair[1]
        self._mat[row, col] = val

    def __matmul__(self, other):
        if isinstance(other, Matrix4x4):
            return Matrix4x4(self._mat @ other._mat)
        elif isinstance(other, Vector3):
            np_vec = other.to_numpy()
            np_vec = np.append(np_vec, 1)
            return Vector3.from_numpy((self._mat @ np_vec)[:3])

    def to_numpy(self):
        return np.copy(self._mat)
