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
from ui.tkframe import tkAnimationFrame, tkUtilFrame
import simple_hopper
import gym

import copy
import pdb
from time import time

from utility.transition_functions import easeInOutCos, easeInOutCubic


def main():
    renderer = Renderer(scale=0.01)
    cam = Camera()
    root = tkinter.Tk()
    animation = None
    pose = None
    env = None
    callback = Callback(cam, root)

    env = gym.make("SimpleHopper-v0")
    # load animation
    # loader = BvhLoader("02_01.bvh")
    # animation = loader.load()

    ## Animation Stitch
    # animation2 = BvhLoader("02_01.bvh").load()
    # animation = animation.stitch(animation2, 30, easeInOutCubic)

    ## Animation Time Warp
    # animation2 = BvhLoader("02_05.bvh").load()
    # pose = animation2.poses[8]
    # pose.rotations[8] = Rotation.from_quaternion(Quaternion())
    # # pose.rotations[22] = Rotation.from_quaternion(Quaternion())
    # animation = animation.warp(pose=pose, frame=170, time=100, trans_func=easeInOutCos)

    root.grid()
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    if animation:
        glrender_frame = tkAnimationFrame(
            renderer, cam, callback, animation, root, width=800, height=600, pose=pose
        )
        glrender_frame.grid(row=0, pady=5)

    playutil_frame = tkUtilFrame(animation, root)
    playutil_frame.grid(row=1, sticky=tkinter.EW)
    scroll_controller = playutil_frame.scroll_controller
    if animation:
        playutil_frame.aniframe_scroll.after(
            int(animation.frame_time * 1000), scroll_controller.next_frame
        )
    interframe_controller = tkInterFrameController(glrender_frame, playutil_frame)
    glrender_frame.after(10, interframe_controller.update_status)

    root.mainloop()


if __name__ == "__main__":
    main()
