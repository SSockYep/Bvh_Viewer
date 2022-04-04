import numpy as np
from data_structure import *

class Test_Vector3():
    def test_initialize():
        test_vec3 = Vector3()
        return test_vec3.x == 0 and test_vec3.y == 0 and test_vec3.z == 0