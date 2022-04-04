import numpy as np
class Vector3:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

    def __str__(self):
        return "Vector3({}, {}, {})".format(self.x, self.y, self.z)

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

class WrongInputException(Exception):
    def __init__(self, inputs, message="WrongInput"):
        self.inputs = inputs
        self.message = message
        super().__init__(self.message)