import numpy as np
from sympy import Matrix
class Vector3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z


    def __str__(self):
        return "Vector3({}, {}, {})".format(self.x, self.y, self.z)

    def __eq__(self, other):
        return  np.isclose(self.x, other.x) and \
            np.isclose(self.y, other.y) and np.isclose(self.z, other.z)

    @staticmethod
    def from_numpy(np_array):
        if type(np_array) != np.ndarray:
            raise WrongInputException(np_array)
        if np_array.size != 3 or len(np_array.shape) != 1:
            raise WrongInputException(np_array)
        new_vector3 = Vector3()
        new_vector3.x = np_array[0]
        new_vector3.y = np_array[1]
        new_vector3.z = np_array[2]
        return new_vector3
    
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
        return np.isclose(self.w, other.w) and np.isclose(self.x, other.x) and \
               np.isclose(self.y, other.y) and np.isclose(self.z, other.z)
    
    def to_matrix(self):
        row0 = np.array([1 - 2*self.y*self.y - 2*self.z*self.z,
                         2*self.x*self.y - 2*self.z*self.w,
                         2*self.x*self.z + 2*self.y*self.w,
                         0])
        row1 = np.array([2*self.x*self.y + 2*self.z*self.w,
                         1 - 2*self.x*self.x - 2*self.z*self.z,
                         2*self.y*self.z - 2*self.x*self.w,
                         0])
        row2 = np.array([2*self.x*self.z - 2*self.y*self.w,
                         2*self.y*self.z + 2*self.x*self.w,
                         1 - 2*self.x*self.x - 2*self.y*self.y,
                         0])
        row3 = np.array([0, 0, 0, 1])
        return Matrix4x4(np.array([row0, row1, row2, row3]))
        
class Matrix4x4: 
    def __init__(self, np_array=np.eye(4,4)):
        if type(np_array) != np.ndarray:
            raise WrongInputException(np_array)
        if np_array.shape != (4, 4):
            raise WrongInputException(np_array)
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
    
    def from_euler(seq, *angles):
        return Matrix4x4(np.array([[1, 0, 0, 0],
                                   [0, np.cos(angles[0]), -np.sin(angles[0]), 0],
                                   [0, np.sin(angles[0]), np.cos(angles[0]), 0],
                                   [0, 0, 0, 1]]))

class WrongInputException(Exception):
    def __init__(self, inputs, message="WrongInput{}"):
        self.inputs = inputs
        self.message = message.format(inputs)
        super().__init__(self.message)
