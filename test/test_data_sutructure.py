from decimal import DivisionByZero
import pytest
import numpy as np
from data_structure.math import *

class Test_Vector3():
    def test_initialize(self):
        test_vec3 = Vector3()
        assert test_vec3.x == 0 and test_vec3.y == 0 and test_vec3.z == 0
    
    def test_vector3_from_numpy(self):
        test_nparray = np.array([1,2,3])
        test_vec3 = Vector3.from_numpy(test_nparray)
        assert test_vec3.x == 1 and test_vec3.y == 2 and test_vec3.z == 3

    def test_wrong_numpy_array(self):
        with pytest.raises(WrongInputException):
            test_nparray = np.array([1,2,3,4])
            Vector3.from_numpy(test_nparray)
    
    def test_vector3_to_numpy(self):
        test_nparray = np.array([4,5,6])
        test_vec3 = Vector3.from_numpy(test_nparray)
        assert test_vec3.to_numpy() == test_nparray


        
            