from re import M
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
        left = Vector3.from_numpy(np.array([3,4,5]))
        right = Vector3.from_numpy(np.array([3.000001, 4.000001, 4.999999]))
        assert left == right
    
    def test_init_from_numbers(self):
        test_vec3 = Vector3(1,2,3)
        assert test_vec3.x == 1 and test_vec3.y == 2 and test_vec3.z == 3
    
    def test_instance_copy(self):
        test_vec1 = Vector3(3.5,4.1,5.2)
        test_vec2 = test_vec1.copy()
        assert test_vec1 == test_vec2 and id(test_vec1) != id(test_vec2)

class TestQuaternion:
    def test_quaternion_init(self):
        assert Quaternion()
    
    def test_init_from_numbers(self):
        quater = Quaternion(1,2,3,4)
        assert quater.w == 1 and quater.x == 2 and \
            quater.y == 3 and quater.z == 4
    
    def test_equal_quaternions(self):
        left = Quaternion(1,2,3,4)
        right = Quaternion(1.00001,2,3,4)
        assert left == right
    
    def test_to_matrix(self):
        quater = Quaternion(np.cos(np.pi/3), np.sin(np.pi/3), 0, 0) # cos(1/3*pi), sin(1/3*pi), 0, 0
        test_nparr = np.array([[1, 0, 0, 0],
                                [0, np.cos(np.pi*2/3), -np.sin(np.pi*2/3), 0],
                                [0, np.sin(np.pi*2/3), np.cos(np.pi*2/3), 0],
                                [0, 0, 0, 1]])
        test_mat = Matrix4x4(test_nparr)
        assert quater.to_matrix() == test_mat
    
    def test_from_matrix(self):
        # matrix and quaternion for rotate pi/6, pi/4, pi/3 (euler xyz)
        test_mat = np.array([[ 0.35355339, -0.5732233 ,  0.73919892, 0.],
                             [ 0.61237244,  0.73919892,  0.28033009, 0.],
                             [-0.70710678,  0.35355339,  0.61237244, 0.],
                             [0., 0., 0., 1.]])
        print(Quaternion.from_matrix(test_mat))
        assert Quaternion.from_matrix(test_mat) == Quaternion(0.82236317, 0.02226003, 0.43967974, 0.36042341)

    def test_from_euler(self):
        assert Quaternion.from_euler('xyz', np.pi/6, np.pi/4, np.pi/3) == Quaternion(0.82236317, 0.02226003, 0.43967974, 0.36042341)

    def test_conjugate(self):
        test_quat = Quaternion(0, np.sin(np.pi/4), 0, np.cos(np.po/4))
        assert test_quat.conjugate() == Quaternion(0, np.sin(np.pi/4), 0, np.cos(np.po/4))
    
    def test_mul(self):
        left = Quaternion(1,2,3,4)
        right = Quaternion(5,6,7,8)
        assert left * right == Quaternion(-60, 12, 30, 24)

class TestMatrix4x4:
    def test_matrix_init(self):
        assert Matrix4x4()

    def test_init_from_nparray(self):
        test_array = np.array([[-0.66227084,  0.97431641,  1.73012908,  0.56201872],
                               [ 0.39474114,  1.70260127, -0.04652928, -0.38493378],
                               [-0.50571852,  1.04094225, -0.40867284, -0.4890231 ],
                               [ 0.23127103,  0.1890786 , -1.8186167 ,  0.00370964]])
        test_mat4x4 = Matrix4x4(test_array)
        assert np.allclose(test_array, test_mat4x4._mat)
    
    def test_get_item(self):
        test_array = np.array([[0, 1,  2, 3],
                               [10, 11,  12, 13],
                               [20, 21,  22, 23],
                               [30, 31,  32, 33]])
        test_mat = Matrix4x4(test_array)
        assert test_mat[0,1] == 1 and test_mat[3,2] == 32 and \
               test_mat[1,1] == 11 and test_mat[0,2] == 2 and \
               np.allclose(test_mat[:,2], np.array([2, 12, 22,32])) and \
               np.allclose(test_mat[1,:], np.array([10, 11, 12, 13]))

    def test_wrong_type_init(self):
        with pytest.raises(WrongInputException):
            test_array = [[0, 1,  2, 3],
                          [10, 11,  12, 32],
                          [20, 21,  22, 23],
                          [30, 31,  32, 33]]
            Matrix4x4(test_array)
    
    def test_wrong_shape_init(self):
        with pytest.raises(WrongInputException):
            test_array1 = np.array([[0, 1,  2, 3, 4],
                                   [10, 11,  12, 13, 14],
                                   [20, 21,  22, 23, 24],
                                   [30, 31,  32, 33, 34]])
            Matrix4x4(test_array1)
            test_array2 = np.array([1,2,3,4])
            Matrix4x4(test_array2)
    
    def test_equal_metrices(self):
        test_array = np.array([[0, 1,  2, 3],
                               [10, 11,  12, 13],
                               [20, 21,  22, 23],
                               [30, 31,  32, 33]])
        left = Matrix4x4(test_array)
        right = Matrix4x4(test_array)
        assert left == right

    def test_matmul(self):
        m1 = Quaternion(np.cos(np.pi/4), 0, np.sin(np.pi/4), 0).to_matrix()
        m2 = Quaternion(np.cos(np.pi/4), 0, -np.sin(np.pi/4), 0).to_matrix()
        assert m1 @ m2 == Matrix4x4(np.eye(4))
    
    def test_mat_vec_mul(self):
        mat = Quaternion(np.cos(np.pi/4), 0, np.sin(np.pi/4), 0).to_matrix()
        vec = Vector3(1,0,0)
        assert mat@vec == Vector3(0, 0, -1)

    def test_rotation_x(self):
        mat = Matrix4x4.from_euler('xyz', np.pi/6, 0, 0)
        assert mat == Matrix4x4(np.array([[1, 0, 0, 0],
                                           [0, np.cos(np.pi/6), -np.sin(np.pi/6), 0],
                                           [0, np.sin(np.pi/6), np.cos(np.pi/6), 0],
                                           [0, 0, 0, 1]]))
    
    def test_rotation_y(self):
        mat = Matrix4x4.from_euler('xyz', 0, np.pi/6, 0)
        assert mat == Matrix4x4(np.array([[np.cos(np.pi/6), 0, np.sin(np.pi/6), 0],
                                           [0, 1, 0, 0],
                                           [-np.sin(np.pi/6), 0, np.cos(np.pi/6), 0],
                                           [0, 0, 0, 1]]))
    
    def test_rotation_z(self):
        mat = Matrix4x4.from_euler('xyz', 0, 0, np.pi/6)
        assert mat == Matrix4x4(np.array([[np.cos(np.pi/6), -np.sin(np.pi/6), 0, 0],
                                          [np.sin(np.pi/6), np.cos(np.pi/6), 0, 0],
                                          [0, 0, 1, 0],
                                          [0, 0, 0, 1]]))
    
    def test_rotation_xyz(self):
        mat = Matrix4x4.from_euler('xyz', np.pi/6, np.pi/4, np.pi/3)
        assert mat == Matrix4x4.from_euler('xyz', np.pi/6, 0, 0) @ \
                      Matrix4x4.from_euler('xyz', 0, np.pi/4, 0) @ \
                      Matrix4x4.from_euler('xyz', 0, 0, np.pi/3)

    def test_rotate_xzy(self):
        mat = Matrix4x4.from_euler('xzy', np.pi/6, np.pi/4, np.pi/3)
        assert mat == Matrix4x4.from_euler('xyz', np.pi/6, 0, 0) @ \
                      Matrix4x4.from_euler('xyz', 0, 0, np.pi/4) @ \
                      Matrix4x4.from_euler('xyz', 0, np.pi/3, 0)
    
    def test_wrong_input_from_euler(self):
        with pytest.raises(WrongInputException):
            Matrix4x4.from_euler('xyy', 0, 0, 0)
        with pytest.raises(WrongInputException):
            Matrix4x4.from_euler('asd', 0, 0, 0)
        with pytest.raises(WrongInputException):
            Matrix4x4.from_euler('xyzy', 0, 0, 0)
        with pytest.raises(WrongInputException):
            Matrix4x4.from_euler('xyz', 0, 0, np.pi, np.pi)
        with pytest.raises(WrongInputException):
            Matrix4x4.from_euler(0, 0, np.pi, np.pi)
