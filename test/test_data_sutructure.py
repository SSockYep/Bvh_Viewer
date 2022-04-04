import pytest
import numpy as np
from data_structure.math import *

class TestVector3():
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
        assert np.allclose(test_vec3.to_numpy(), test_nparray)

    def test_vector3_to_string(self):
        test_vec3 = Vector3.from_numpy(np.array([1,2,3]))
        assert str(test_vec3) == "Vector3(1, 2, 3)"

    def test_wrong_type_from_numpy(self):
        with pytest.raises(WrongInputException):
            Vector3.from_numpy([1,2,3])
        
    def test_equal_vectors(self):
        left = Vector3.from_numpy(np.array[3,4,5])
        right = Vector3.from_numpy(np.array[3.000001, 4.000001, 4.999999])
        assert left == right