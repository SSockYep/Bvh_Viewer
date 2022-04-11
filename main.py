import numpy as np
import glfw

from OpenGL.GL import *
from OpenGL.GLU import *

from data_structure.math import *
from ui.renderer import *
from ui.camera import Camera
from ui.callback import Callback
from utility.bvh_loader import BvhLoader


def main():
    if not glfw.init():
        return
    window = glfw.create_window(680, 480, "test", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    renderer = Renderer()
    cam = Camera()
    animation = BvhLoader("test.bvh").parse()
    callback = Callback(cam, window)
    glfw.set_mouse_button_callback(window, callback.mouse_callback)
    glfw.set_cursor_pos_callback(window, callback.cursor_callback)
    i = 0
    while not glfw.window_should_close(window):
        i += 1
        i = i % animation.frame
        glfw.poll_events()
        renderer.clear()
        renderer.render_perspective(cam)
        renderer.render_global_axis()
        renderer.render_pose(animation.get_pose(i))
        glfw.swap_buffers(window)
    glfw.terminate()


if __name__ == "__main__":
    main()
