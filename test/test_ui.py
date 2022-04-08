import numpy as np
import pytest
from data_structure.math import Vector3
from ui.renderer import Renderer
from ui.camera import Camera

from utility.transform import Rotation

class TestRenderer:
    def test_init(self):
        assert Renderer()

    def test_render_line(self):
        renderer = Renderer()
        a = Vector3(0,0,0)
        b = Vector3(1,1,1)
        assert renderer.render_line(a, b)


class TestCamera:
    def test_init(self):
        cam = Camera(pos=Vector3(1,1,1), lookat=Vector3(0,0,0))
        assert cam
    
    def test_move(self):
        pass