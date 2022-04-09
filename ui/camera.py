import numpy as np
from data_structure.math import *
from utility.transform import Rotation
from OpenGL.GLU import *


class Camera:
    def __init__(self, pos=Vector3(0.0, 1.0, 5.0), lookat=Vector3(0.0, 0.0, 0.0)):
        self.pos = pos
        self.lookat = lookat

    def move(self, x_move, y_move):
        cam_x, cam_y, cam_z = self._get_local_axis()

        self.pos = self.pos + cam_x * x_move + cam_y * y_move
        self.lookat = self.lookat + cam_x * x_move + cam_y * y_move

    def rotate(self, x, y):
        cam_x, cam_y, cam_z = self._get_local_axis()
        cam_x = cam_x * np.sin(x / 2)
        cam_y = cam_y * np.sin(y / 2)
        print(cam_z)
        rot_x = Rotation.from_quaternion(
            Quaternion(np.cos(x / 2), cam_x.x, cam_x.y, cam_x.z)
        )

        if cam_z.y < -0.9 or cam_z.y > 0.9:
            rot_y = Rotation.from_quaternion(Quaternion(1, 0, 0, 0))
            print("한계")
        else:
            rot_y = Rotation.from_quaternion(
                Quaternion(np.cos(y / 2), cam_y.x, cam_y.y, cam_y.z)
            )
        local_pos = self.pos - self.lookat
        rotated = rot_x.rotate(local_pos)
        rotated = rot_y.rotate(rotated)
        self.pos = rotated + self.lookat

    def _get_local_axis(self):
        cam_z = self.pos - self.lookat
        cam_z = cam_z / cam_z.magnitude()
        cam_x = Vector3(0, 1, 0) * cam_z
        cam_x = cam_x / cam_x.magnitude()
        cam_y = cam_z * cam_x
        cam_y = cam_y / cam_y.magnitude()
        return (cam_x, cam_y, cam_z)

