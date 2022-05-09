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

import copy
import pdb

from utility.transition_functions import easeInOutCos


def main():
    renderer = Renderer(scale=0.05)
    cam = Camera()
    root = tkinter.Tk()
    callback = Callback(cam, root)
    loader = BvhLoader("01_01.bvh")
    pose = None
    # pose = BvhLoader("01_02.bvh").load().poses[4]
    # pose.root_translation = pose.root_translation + Vector3(15, 0, 0)
    animation = loader.load()
    pose = copy.deepcopy(animation.poses[1695])
    pose.rotations[18] = Rotation.from_quaternion(Quaternion(1, 0, 0, 0))

    animation = animation.warp(pose=pose, frame=1695, time=30, trans_func=easeInOutCos)

    root.grid()
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    glrender_frame = tkRenderFrame(
        renderer, cam, callback, animation, root, width=800, height=600, pose=pose
    )
    glrender_frame.grid(row=0, pady=5)

    playutil_frame = tkUtilFrame(animation, root)
    playutil_frame.grid(row=1, sticky=tkinter.EW)
    scroll_controller = playutil_frame.scroll_controller
    playutil_frame.aniframe_scroll.after(
        int(animation.frame_time * 1000), scroll_controller.next_frame
    )
    interframe_controller = tkInterFrameController(glrender_frame, playutil_frame)
    glrender_frame.after(10, interframe_controller.update_status)

    root.mainloop()


if __name__ == "__main__":
    main()
