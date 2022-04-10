from lzma import MODE_FAST
import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *
import glfw
from prometheus_client import Enum
from .camera import Camera


class Mouse(Enum):
    NONE = 1
    LBUTTON = 2
    RBUTTON = 3
    MBUTTON = 4


class Callback:
    def __init__(self, cam: Camera, window):
        self.cam = cam
        self.mouse_x, self.mouse_y = glfw.get_cursor_pos(window)
        self.mouse_button = Mouse.NONE

    def cursor_callback(self, window, cur_x, cur_y):
        if self.mouse_button == Mouse.MBUTTON:
            self.cam.move((self.mouse_x - cur_x) / 100, (cur_y - self.mouse_y) / 100)
        elif self.mouse_button == Mouse.LBUTTON:
            self.cam.rotate((cur_y - self.mouse_y) / 100, (cur_x - self.mouse_x) / 100)
        elif self.mouse_button == Mouse.RBUTTON:
            self.cam.zoom((self.mouse_y - cur_y) / 10)
        self.mouse_x = cur_x
        self.mouse_y = cur_y

    def mouse_callback(self, window, button, action, mods):
        if action == glfw.PRESS and self.mouse_button == Mouse.NONE:
            if button == glfw.MOUSE_BUTTON_MIDDLE:
                self.mouse_button = Mouse.MBUTTON
            elif button == glfw.MOUSE_BUTTON_LEFT:
                self.mouse_button = Mouse.LBUTTON
            elif button == glfw.MOUSE_BUTTON_RIGHT:
                self.mouse_button = Mouse.RBUTTON
        elif action == glfw.RELEASE:
            self.mouse_button = Mouse.NONE
