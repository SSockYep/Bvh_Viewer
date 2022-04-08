import numpy as np

class Vector3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "Vector3({}, {}, {})".format(self.x, self.y, self.z)

    def __eq__(self, other):
        return np.isclose(self.x, other.x) and \
            np.isclose(self.y, other.y) and np.isclose(self.z, other.z)

    @classmethod
    def from_numpy(cls, np_array):
        if type(np_array) != np.ndarray:
            raise ValueError
        if np_array.size != 3 or len(np_array.shape) != 1:
            raise ValueError
        return cls(np_array[0], np_array[1], np_array[2])

    def to_numpy(self):
        return np.array([self.x, self.y, self.z])

    def copy(self):
        return Vector3(self.x, self.y, self.z)


class Quaternion:
    def __init__(self, w=1, x=0, y=0, z=0):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        return np.isclose(self.w, other.w) and np.isclose(self.x, other.x) \
               and np.isclose(self.y, other.y) and np.isclose(self.z, other.z)

    def __str__(self):
        return "Quaternion({}, {}, {}, {})".format(self.w, self.x, self.y, self.z)
    
    def __mul__(self, other):
        if not isinstance(other, Quaternion):
            assert TypeError(other)
        a, b, c, d = self.w, self.x, self.y, self.z
        e, f, g, h = other.w, other.x, other.y, other.z
        res = Quaternion((a*e - b*f - c*g - d*h), (a*f + b*e + c*h - d*g),
                          (a*g - b*h + c*e + d*f), (a*h + b*g - c*f + d*e))
        return res

    def conjugate(self):
        return Quaternion(self.w, -self.x, -self.y, -self.z)

class Matrix4x4: 
    def __init__(self, np_array=np.eye(4,4)):
        if type(np_array) != np.ndarray:
            raise ValueError
        if np_array.shape != (4, 4):
            raise ValueError
        self._mat = np.copy(np_array)

    def __eq__(self, other):
        return np.allclose(self._mat, other._mat)

    def __getitem__(self, pair):
        row = pair[0]
        col = pair[1]
        return self._mat[row, col]
    
    def __matmul__(self, other):
        if isinstance(other, Matrix4x4):
            return Matrix4x4(self._mat @ other._mat)
        elif isinstance(other, Vector3):
            np_vec = other.to_numpy()
            np_vec = np.append(np_vec, 1)
            return Vector3.from_numpy((self._mat@np_vec)[:3])
    
    @classmethod
    def from_euler(cls, seq, *angles):
        def rotate(axis, angle):
            if axis == 'x' or axis == 'X':
                return Matrix4x4(np.array([[1, 0, 0, 0],
                                           [0, np.cos(angle), -np.sin(angle), 0],
                                           [0, np.sin(angle), np.cos(angle), 0],
                                           [0, 0, 0, 1]]))
            elif axis == 'y' or axis == 'Y':
                return Matrix4x4(np.array([[np.cos(angle), 0, np.sin(angle), 0],
                                           [0, 1, 0, 0],
                                           [-np.sin(angle), 0, np.cos(angle), 0],
                                           [0, 0, 0, 1]]))
            elif axis == 'z' or axis == 'Z':
                return Matrix4x4(np.array([[np.cos(angle), -np.sin(angle), 0, 0],
                                           [np.sin(angle), np.cos(angle), 0, 0],
                                           [0, 0, 1, 0],
                                           [0, 0, 0, 1]]))
            else:
                raise ValueError
        if type(seq) != str:
            raise ValueError
        if len(seq) != 3:
            raise ValueError
        if seq[0]==seq[1] or seq[1] == seq[2]:
            raise ValueError
        if seq[0] not in 'xyz' or seq[1] not in 'xyz' or seq[2] not in 'xyz':
            raise ValueError
        if len(angles) != 3:
            raise ValueError
        mat0 = rotate(seq[0], angles[0])
        mat1 = rotate(seq[1], angles[1])
        mat2 = rotate(seq[2], angles[2])
        return cls((mat0@mat1@mat2)._mat)
