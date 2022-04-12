import numpy as np
from data_structure.math import *
from utility.transform import Rotation
from OpenGL.GLU import *


class Camera:
    def __init__(self, pos=Vector3(5.0, 2.0, 5.0), lookat=Vector3(0.0, 0.0, 0.0)):
        self.pos = pos
        self.lookat = lookat
        self.angle = 45

    def move(self, x_move, y_move):
        cam_x, cam_y, cam_z = self._get_local_axis()

        self.pos = self.pos + cam_x * x_move + cam_y * y_move
        self.lookat = self.lookat + cam_x * x_move + cam_y * y_move

    def rotate(self, x, y):
        # moving mouse vertical(y) => rotate about local axis x(cam_x)
        # moving mouse horizontal(y) => rotate about local axis y(cam_y)
        cam_x, cam_y, cam_z = self._get_local_axis()
        local_pos = self.pos - self.lookat
        if cam_z.y < -0.99 and y > 0:
            rot_x = Rotation.from_quaternion(Quaternion(1, 0, 0, 0))
        elif cam_z.y > 0.99 and y < 0:
            rot_x = Rotation.from_quaternion(Quaternion(1, 0, 0, 0))
        else:
            cam_x = cam_x * np.sin(y / 2)
            rot_x = Rotation.from_quaternion(
                Quaternion(np.cos(y / 2), cam_x.x, cam_x.y, cam_x.z)
            )
        cam_y = cam_y * np.sin(x / 2)
        rot_y = Rotation.from_quaternion(
            Quaternion(np.cos(x / 2), cam_y.x, cam_y.y, cam_y.z)
        )
        rotated = rot_x.rotate(local_pos)
        rotated = rot_y.rotate(rotated)

        self.pos = rotated + self.lookat

    def zoom(self, value):
        self.angle += value
        if self.angle >= 180:
            self.angle = 179
        elif self.angle <= 0:
            self.angle = 1

    def _get_local_axis(self):
        cam_z = self.pos - self.lookat
        cam_z = cam_z / cam_z.magnitude()
        cam_x = Vector3(0, 1, 0) * cam_z
        cam_x = cam_x / cam_x.magnitude()
        cam_y = cam_z * cam_x
        cam_y = cam_y / cam_y.magnitude()
        return (cam_x, cam_y, cam_z)
