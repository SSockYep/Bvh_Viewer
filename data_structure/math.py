import numpy as np
class Vector3:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

    @staticmethod
    def from_numpy(np_array):
        new_vector3 = Vector3()
        new_vector3.x = np_array[0]
        new_vector3.y = np_array[1]
        new_vector3.z = np_array[2]
        return new_vector3