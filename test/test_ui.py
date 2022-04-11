import numpy as np
import pytest
from data_structure.math import Vector3
from gl_render.renderer import Renderer
from gl_render.camera import Camera

from utility.transform import Rotation


class TestRenderer:
    def test_init(self):
        assert Renderer()


class TestCamera:
    def test_init(self):
        cam = Camera(pos=Vector3(1, 1, 1), lookat=Vector3(0, 0, 0))
        assert cam

    def test_move(self):
        cam = Camera(pos=Vector3(0, 0, 5), lookat=Vector3(0, 0, 0))
        cam.move(1, 1)
        assert cam.pos == Vector3(1, 1, 5) and cam.lookat == Vector3(1, 1, 0)

    def test_rotate(self):
        cam = Camera(pos=Vector3(5, 0, 0), lookat=Vector3(0, 0, 0))
        cam.rotate(np.pi / 2, 0)
        assert cam.pos == Vector3(0, 0, -5) and cam.lookat == Vector3(0, 0, 0)
