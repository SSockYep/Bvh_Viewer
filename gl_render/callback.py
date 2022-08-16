import numpy as np
import tkinter
from OpenGL.GL import *
from OpenGL.GLU import *
from enum import Enum
from .camera import Camera


class Mouse(Enum):
    NONE = 0
    LBUTTON = 1
    RBUTTON = 2
    MBUTTON = 3


class Callback:
    def __init__(self, cam: Camera, window: tkinter.Tk):
        self.cam = cam
        self.mouse_x = window.winfo_pointerx() - window.winfo_rootx()
        self.mouse_y = window.winfo_pointery() - window.winfo_rooty()
        self.mouse_button = Mouse.NONE

    def cursor_move_callback(self, event):
        if self.mouse_button == Mouse.MBUTTON:
            print("move")
            self.cam.move(
                (self.mouse_x - event.x) / 100, (event.y - self.mouse_y) / 100
            )
        elif self.mouse_button == Mouse.LBUTTON:
            self.cam.rotate(
                (event.x - self.mouse_x) / 100, (event.y - self.mouse_y) / 100
            )
        elif self.mouse_button == Mouse.RBUTTON:
            self.cam.zoom((self.mouse_y - event.y) / 10)
        self.mouse_x = event.x
        self.mouse_y = event.y

    def lclick_callback(self, event):
        self.mouse_button = Mouse.LBUTTON

    def mclick_callback(self, event):
        self.mouse_button = Mouse.MBUTTON

    def rclick_callback(self, event):
        self.mouse_button = Mouse.RBUTTON

    def release_callback(self, envent):
        self.mouse_button = Mouse.NONE
