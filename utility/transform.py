import numpy as np
from copy import copy
from data_structure.math import *

class Rotation:
    def __init__(self, q: Quaternion = Quaternion()):
        self.quaternion = copy(q)

    def __eq__(self, other):
        if isinstance(other, Rotation):
            return self.quaternion == other.quaternion
        return False

    @classmethod
    def from_matrix(cls, mat: Matrix4x4):
        if not np.allclose(mat[:, 3], [0,0,0,1]):
            raise ValueError
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
        if not np.isclose(np.array([w,x,y,z])@np.array([w,x,y,z]), 1):
            raise ValueError
        return cls(Quaternion(w, x, y, z))

    @classmethod
    def from_euler(cls, seq:str='xyz', *angles):        
        if len(seq) != 3 or len(angles) != 3:
            raise ValueError
        if seq[0]==seq[1] or seq[1] == seq[2]:
            raise ValueError
        if seq[0] not in 'xyz' or seq[1] not in 'xyz' or seq[2] not in 'xyz':
            raise ValueError
        def rotate(axis, angle):
            params = [np.cos(angle/2), 0, 0, 0]
            i = int()
            if str.lower(axis) == 'x':
                i = 1
            elif str.lower(axis) == 'y':
                i = 2
            elif str.lower(axis) == 'z':
                i = 3
            else:
                raise ValueError
            params[i] = np.sin(angle/2)
            return Quaternion(params[0], params[1], params[2], params[3])
        q = []
        for i in range(3):
            q.append(rotate(seq[i], angles[i]))
        return cls(q[2]*q[1]*q[0])

    def to_quaternion(self):
        return self.quaternion
    
    def to_matrix(self):
        q = self.quaternion
        row0 = np.array([1 - 2*q.y*q.y - 2*q.z*q.z,
                         2*q.x*q.y - 2*q.z*q.w,
                         2*q.x*q.z + 2*q.y*q.w,
                         0])
        row1 = np.array([2*q.x*q.y + 2*q.z*q.w,
                         1 - 2*q.x*q.x - 2*q.z*q.z,
                         2*q.y*q.z - 2*q.x*q.w,
                         0])
        row2 = np.array([2*q.x*q.z - 2*q.y*q.w,
                         2*q.y*q.z + 2*q.x*q.w,
                         1 - 2*q.x*q.x - 2*q.y*q.y,
                         0])
        row3 = np.array([0, 0, 0, 1])
        return Matrix4x4(np.array([row0, row1, row2, row3])) 
