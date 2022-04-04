import numpy as np
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

class WrongInputException(Exception):
    def __init__(self, inputs, message="WrongInput"):
        self.inputs = inputs
        self.message = message
        super().__init__(self.message)

class Matrix4x4:
    def __init__(self, np_array=np.eye(4,4)):
        self._mat = np_array

    def __getitem__(self, row, col):
        return self._mat[row, col]