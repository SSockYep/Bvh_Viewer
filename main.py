import numpy as np
import tkinter

from OpenGL.GL import *
from OpenGL.GLU import *

from data_structure.math import *
from gl_render.renderer import *
from gl_render.camera import Camera
from gl_render.callback import Callback
from ui.tkutil import tkInterFrameController
from utility.bvh_loader import BvhLoader
from ui.tkframe import tkRenderFrame, tkUtilFrame

import pdb

root = tkinter.Tk()


def main():
    renderer = Renderer()
    cam = Camera()
    # root = tkinter.Tk()
    tcl_root = tkinter.Tcl()
    callback = Callback(cam, root)
    loader = BvhLoader("test.bvh")

    animation = loader.parse()
    root.grid()
    glrender_frame = tkRenderFrame(
        renderer, cam, callback, animation, root, width=800, height=600
    )
    glrender_frame.grid(row=0)
    playutil_frame = tkUtilFrame(animation, root, width=800)
    playutil_frame.grid(row=1, sticky=tkinter.EW)
    scroll_controller = playutil_frame.scroll_controller
    playutil_frame.aniframe_scroll.after(
        int(animation.frame_time * 1000), scroll_controller.next_frame
    )
    interframe_controoler = tkInterFrameController(glrender_frame, playutil_frame)
    glrender_frame.after(10, interframe_controoler.update_status)

    root.mainloop()


if __name__ == "__main__":
    main()
