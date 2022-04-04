import numpy as np
from data_structure.math import Vector3

class Test_Vector3():
    def test_initialize(self):
        test_vec3 = Vector3()
        return test_vec3.x == 0 and test_vec3.y == 0 and test_vec3.z == 0
    
    def test_vector3_from_numpy(self):
        test_nparray = np.array([1,2,3])
        test_vec3 = Vector3.from_numpy(test_nparray)
        return test_vec3.x == 1 and test_vec3.y == 2 and test_vec3.z == 3