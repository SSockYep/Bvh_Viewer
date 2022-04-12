import numpy as np
import tkinter

from OpenGL.GL import *
from OpenGL.GLU import *

from data_structure.math import *
from gl_render.renderer import *
from gl_render.camera import Camera
from gl_render.callback import Callback
from utility.bvh_loader import BvhLoader
from ui.tkframe import tkRenderFrame, tkPlayFrame

import pdb


def main():
    renderer = Renderer()
    cam = Camera()
    root = tkinter.Tk()
    callback = Callback(cam, root)

    root.grid()
    glrender_frame = tkRenderFrame(renderer, cam, callback, root, width=800, height=600)
    glrender_frame.grid(row=0)
    playutil_frame = tkPlayFrame(100, root, width=800)
    playutil_frame.grid(row=1, sticky=tkinter.EW)
    root.mainloop()


if __name__ == "__main__":
    main()
