import pytest
import numpy as np
from data_structure.math import *
from data_structure.animation import *
from data_structure.bvh_tree import *


class TestVector3:
    def test_initialize(self):
        test_vec3 = Vector3()
        assert test_vec3.x == 0 and test_vec3.y == 0 and test_vec3.z == 0

    def test_vector3_from_numpy(self):
        test_nparray = np.array([1, 2, 3])
        test_vec3 = Vector3.from_numpy(test_nparray)
        assert test_vec3.x == 1 and test_vec3.y == 2 and test_vec3.z == 3

    def test_wrong_numpy_array(self):
        with pytest.raises(ValueError):
            test_nparray = np.array([1, 2, 3, 4])
            Vector3.from_numpy(test_nparray)

    def test_vector3_to_numpy(self):
        test_nparray = np.array([4, 5, 6])
        test_vec3 = Vector3.from_numpy(test_nparray)
        assert np.allclose(test_vec3.to_numpy(), test_nparray)

    def test_vector3_to_string(self):
        test_vec3 = Vector3.from_numpy(np.array([1, 2, 3]))
        assert str(test_vec3) == "Vector3(1, 2, 3)"

    def test_wrong_type_from_numpy(self):
        with pytest.raises(ValueError):
            Vector3.from_numpy([1, 2, 3])

    def test_equal_vectors(self):
        left = Vector3.from_numpy(np.array([3, 4, 5]))
        right = Vector3.from_numpy(np.array([3.000001, 4.000001, 4.999999]))
        assert left == right

    def test_init_from_numbers(self):
        test_vec3 = Vector3(1, 2, 3)
        assert test_vec3.x == 1 and test_vec3.y == 2 and test_vec3.z == 3

    def test_instance_copy(self):
        test_vec1 = Vector3(3.5, 4.1, 5.2)
        test_vec2 = test_vec1.copy()
        assert test_vec1 == test_vec2 and id(test_vec1) != id(test_vec2)

    def test_magnitude(self):
        test_vec = Vector3(3, 4, 5)
        assert test_vec.magnitude() == np.sqrt(3 ** 2 + 4 ** 2 + 5 ** 2)

    def test_add(self):
        test_vec1 = Vector3(1, 2, 3)
        test_vec2 = Vector3(4, 5, 6)
        assert test_vec1 + test_vec2 == Vector3(5, 7, 9)

    def test_sub(self):
        test_vec1 = Vector3(1, 2, 3)
        test_vec2 = Vector3(4, 5, 6)
        assert test_vec1 - test_vec2 == Vector3(-3, -3, -3)

    def test_div_by_scalar(self):
        test_vec = Vector3(3, 6, 9)
        assert test_vec / 3 == Vector3(1, 2, 3)

    def test_dot_product(self):
        assert Vector3(1, 2, 3) @ Vector3(4, 5, 6) == 4 + 10 + 18

    def test_cross_product(self):
        vec1 = Vector3(1, 2, 3)
        vec2 = Vector3(4, 5, 6)
        res_vec = vec1 * vec2
        assert res_vec == Vector3(-3, 6, -3)

    def test_mul_by_scalar(self):
        vec = Vector3(1, 2, 3)
        scal = 5
        assert vec * scal == Vector3(5, 10, 15)


class TestQuaternion:
    def test_quaternion_init(self):
        assert Quaternion()

    def test_init_from_numbers(self):
        quater = Quaternion(1, 2, 3, 4)
        assert quater.w == 1 and quater.x == 2 and quater.y == 3 and quater.z == 4

    def test_equal_quaternions(self):
        left = Quaternion(1, 2, 3, 4)
        right = Quaternion(1.00001, 2, 3, 4)
        assert left == right

    def test_conjugate(self):
        test_quat = Quaternion(0, np.sin(np.pi / 4), 0, np.cos(np.pi / 4))
        assert test_quat.conjugate() == Quaternion(
            0, -np.sin(np.pi / 4), 0, -np.cos(np.pi / 4)
        )

    def test_mul(self):
        left = Quaternion(1, 2, 3, 4)
        right = Quaternion(5, 6, 7, 8)
        assert left * right == Quaternion(-60, 12, 30, 24)

    def test_to_numpy_with_dtype(self):
        vec = Vector3(1, 2, 3)
        assert vec.to_numpy(np.uint32).dtype == np.uint32


class TestMatrix4x4:
    def test_matrix_init(self):
        assert Matrix4x4()

    def test_init_from_nparray(self):
        test_array = np.array(
            [
                [-0.66227084, 0.97431641, 1.73012908, 0.56201872],
                [0.39474114, 1.70260127, -0.04652928, -0.38493378],
                [-0.50571852, 1.04094225, -0.40867284, -0.4890231],
                [0.23127103, 0.1890786, -1.8186167, 0.00370964],
            ]
        )
        test_mat4x4 = Matrix4x4(test_array)
        assert np.allclose(test_array, test_mat4x4._mat)

    def test_get_item(self):
        test_array = np.array(
            [[0, 1, 2, 3], [10, 11, 12, 13], [20, 21, 22, 23], [30, 31, 32, 33]]
        )
        test_mat = Matrix4x4(test_array)
        assert (
            test_mat[0, 1] == 1
            and test_mat[3, 2] == 32
            and test_mat[1, 1] == 11
            and test_mat[0, 2] == 2
            and np.allclose(test_mat[:, 2], np.array([2, 12, 22, 32]))
            and np.allclose(test_mat[1, :], np.array([10, 11, 12, 13]))
        )

    def test_wrong_type_init(self):
        with pytest.raises(ValueError):
            test_array = [
                [0, 1, 2, 3],
                [10, 11, 12, 32],
                [20, 21, 22, 23],
                [30, 31, 32, 33],
            ]
            Matrix4x4(test_array)

    def test_wrong_shape_init(self):
        with pytest.raises(ValueError):
            test_array1 = np.array(
                [
                    [0, 1, 2, 3, 4],
                    [10, 11, 12, 13, 14],
                    [20, 21, 22, 23, 24],
                    [30, 31, 32, 33, 34],
                ]
            )
            Matrix4x4(test_array1)
            test_array2 = np.array([1, 2, 3, 4])
            Matrix4x4(test_array2)

    def test_equal_metrices(self):
        test_array = np.array(
            [[0, 1, 2, 3], [10, 11, 12, 13], [20, 21, 22, 23], [30, 31, 32, 33]]
        )
        left = Matrix4x4(test_array)
        right = Matrix4x4(test_array)
        assert left == right

    def test_matmul(self):
        m1 = Matrix4x4(
            np.array([[0, 0, 1, 0], [0, 1, 0, 0], [-1, 0, 0, 0], [0, 0, 0, 1]])
        )
        m2 = Matrix4x4(
            np.array([[0, 0, -1, 0], [0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1]])
        )
        assert m1 @ m2 == Matrix4x4(np.eye(4))

    def test_mat_vec_mul(self):
        mat = Matrix4x4(
            np.array([[0, 0, 1, 0], [0, 1, 0, 0], [-1, 0, 0, 0], [0, 0, 0, 1]])
        )
        vec = Vector3(1, 0, 0)
        assert mat @ vec == Vector3(0, 0, -1)


class TestPose:
    def test_init(self):
        root = Node()
        node1 = Node()
        node2 = Node()
        node1.set_parent(root)
        node2.set_parent(root)
        assert Pose(root)


class TestNode:
    def test_node_initialize(self):
        assert Node() != None

    def test_offset(self):
        node = Node()
        node.offset = Vector3(1, 1, 1)
        assert node.offset == Vector3(1, 1, 1)

    def test_set_offset_on_init(self):
        node = Node(Vector3(1, 1, 1))
        assert node.offset == Vector3(1, 1, 1)

    def test_set_node_name(self):
        node = Node()
        node.set_name("test_name")
        assert node.get_name() == "test_name"

    def test_set_name_on_init(self):
        node = Node(offset=Vector3(1, 1, 1), name="test_name")
        assert node.get_name() == "test_name"

    def test_add_child(self):
        node = Node(name="parent")
        child_node = Node(name="child")
        node.add_child(child_node)
        assert node.children[0] == child_node

    def test_set_parent(self):
        node = Node(name="child")
        parent_node = Node(name="parent")
        node.set_parent(parent_node)
        assert node.parent == parent_node and node in parent_node.children

    def test_delete_child(self):
        node = Node(name="child")
        parent_node = Node(name="parent")
        parent_node.add_child(node)
        parent_node.delete_child("child")
        assert node not in parent_node.children

    def test_get_hier(self):
        root = Node(name="root")
        node1 = Node(name="node1")
        node2 = Node(name="node2")
        node3 = Node(name="node3")
        node1.set_parent(root)
        node2.set_parent(root)
        node3.set_parent(node1)

        assert root.get_hier() == "root\n  node1\n    node3\n  node2\n"

    def test_is_root(self):
        node = Node()
        assert node.is_root()
