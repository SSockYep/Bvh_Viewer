import numpy as np
from sympy import Matrix
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

    @classmethod
    def from_numpy(cls, np_array):
        if type(np_array) != np.ndarray:
            raise WrongInputException(np_array)
        if np_array.size != 3 or len(np_array.shape) != 1:
            raise WrongInputException(np_array)
        return cls(np_array[0], np_array[1], np_array[2])
    
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
    
    def __eq__(self, other):
        return np.isclose(self.w, other.w) and np.isclose(self.x, other.x) and \
               np.isclose(self.y, other.y) and np.isclose(self.z, other.z)

    def __str__(self):
        return "Quaternion({}, {}, {}, {})".format(self.w, self.x, self.y, self.z)
    
    def to_matrix(self):
        row0 = np.array([1 - 2*self.y*self.y - 2*self.z*self.z,
                         2*self.x*self.y - 2*self.z*self.w,
                         2*self.x*self.z + 2*self.y*self.w,
                         0])
        row1 = np.array([2*self.x*self.y + 2*self.z*self.w,
                         1 - 2*self.x*self.x - 2*self.z*self.z,
                         2*self.y*self.z - 2*self.x*self.w,
                         0])
        row2 = np.array([2*self.x*self.z - 2*self.y*self.w,
                         2*self.y*self.z + 2*self.x*self.w,
                         1 - 2*self.x*self.x - 2*self.y*self.y,
                         0])
        row3 = np.array([0, 0, 0, 1])
        return Matrix4x4(np.array([row0, row1, row2, row3]))
    
    @classmethod
    def from_matrix(cls, mat):
        if not np.allclose(mat[:, 3], [0,0,0,1]):
            raise WrongInputException(mat, "Wrong Input (matrix has translation: {})") 
        tr = np.array([mat[0,0], mat[1,1], mat[2,2],  
                       mat[0,0]+mat[1,1]+mat[2,2]])
        arg_max = tr.argmax()
        if arg_max == 3:
            w4 = np.sqrt(tr[3]+1)*2
            w = w4 / 4
            x = (mat[2,1]-mat[1,2]) / w4
            y = (mat[0,2]-mat[2,0]) / w4
            z = (mat[1,0]-mat[0,1]) / w4
        elif arg_max == 0:
            x4 = np.sqrt(1+tr[0]-tr[1]-tr[2])
            w = (mat[2,1]-mat[1,2]) / x4
            x = w4 / 4
            y = (mat[0,1]+mat[1,0]) / x4
            z = (mat[0,2]+mat[2,0]) / x4
        elif arg_max == 1:
            y4 = np.sqrt(1+tr[1]-tr[2]-tr[0])
            w = (mat[0,2]-mat[2,0]) / y4
            x = (mat[0,1]+mat[1,0]) / y4
            y = y4 / 4
            z = (mat[1,2]+mat[2,1]) / y4
        else:
            z4 = np.sqrt(1+tr[2]-tr[0]-tr[1])
            w = (mat[1,0]-mat[0,1]) / z4
            x = (mat[0,2]+mat[2,0]) / z4
            y = (mat[1,2]+mat[2,1]) / z4
            z = z4 / 4
        return cls(w, x, y, z)

        if np.array([w,x,y,z])@np.array([w,x,y,z]) != 1:
            raise WrongInputException(mat, "wrong input (matrix has transform not rotation {})") 
        return cls(w, x, y, z)
        
class Matrix4x4: 
    def __init__(self, np_array=np.eye(4,4)):
        if type(np_array) != np.ndarray:
            raise WrongInputException(np_array)
        if np_array.shape != (4, 4):
            raise WrongInputException(np_array)
        self._mat = np.copy(np_array)

    def __eq__(self, other):
        return np.allclose(self._mat, other._mat)

    def __getitem__(self, pair):
        row = pair[0]
        col = pair[1]
        return self._mat[row, col]
    
    def __matmul__(self, other):
        if isinstance(other, Matrix4x4):
            return Matrix4x4(self._mat @ other._mat)
        elif isinstance(other, Vector3):
            np_vec = other.to_numpy()
            np_vec = np.append(np_vec, 1)
            return Vector3.from_numpy((self._mat@np_vec)[:3])
    
    @classmethod
    def from_euler(cls, seq, *angles):
        def rotate(axis, angle):
            if axis == 'x' or axis == 'X':
                return Matrix4x4(np.array([[1, 0, 0, 0],
                                           [0, np.cos(angle), -np.sin(angle), 0],
                                           [0, np.sin(angle), np.cos(angle), 0],
                                           [0, 0, 0, 1]]))
            elif axis == 'y' or axis == 'Y':
                return Matrix4x4(np.array([[np.cos(angle), 0, np.sin(angle), 0],
                                           [0, 1, 0, 0],
                                           [-np.sin(angle), 0, np.cos(angle), 0],
                                           [0, 0, 0, 1]]))
            elif axis == 'z' or axis == 'Z':
                return Matrix4x4(np.array([[np.cos(angle), -np.sin(angle), 0, 0],
                                           [np.sin(angle), np.cos(angle), 0, 0],
                                           [0, 0, 1, 0],
                                           [0, 0, 0, 1]]))
            else:
                raise WrongInputException(seq)
        if type(seq) != str:
            raise WrongInputException(seq, message="Wrong Input (type of {})")
        if len(seq) != 3:
            raise WrongInputException(seq, message="Wrong Input (len of {})")
        if seq[0]==seq[1] or seq[1] == seq[2]:
            raise WrongInputException(seq, message="Wrong Input (repete same axis: {})")
        if seq[0] not in 'xyz' or seq[1] not in 'xyz' or seq[2] not in 'xyz':
            raise WrongInputException(seq, message="Wrong Input (character not in 'xyz' included: {})")
        if len(angles) != 3:
            raise WrongInputException(angles, message="Wrong Input (len of angles: {})")
        mat0 = rotate(seq[0], angles[0])
        mat1 = rotate(seq[1], angles[1])
        mat2 = rotate(seq[2], angles[2])
        return cls((mat0@mat1@mat2)._mat)

class WrongInputException(Exception):
    def __init__(self, inputs, message="WrongInput{}"):
        self.inputs = inputs
        self.message = message.format(inputs)
        super().__init__(self.message)
