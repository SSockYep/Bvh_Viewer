import numpy as np
class Vector3:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

    @staticmethod
    def from_numpy(np_array):
        if np_array.size != 3 or len(np_array.shape) != 1:
            raise WrongInputException(np_array)
        new_vector3 = Vector3()
        new_vector3.x = np_array[0]
        new_vector3.y = np_array[1]
        new_vector3.z = np_array[2]
        return new_vector3

class WrongInputException(Exception):
    def __init__(self, inputs, message="WrongInput"):
        self.inputs = inputs
        self.message = message
        super().__init__(self.message)