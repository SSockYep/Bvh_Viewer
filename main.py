import numpy as np
import glfw

from OpenGL.GL import *
from OpenGL.GLU import *

from data_structure.math import *
from ui.renderer import *
from ui.camera import Camera


def main():
    if not glfw.init():
        return
    window = glfw.create_window(680,480, 'test', None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    renderer = Renderer()
    cam = Camera()
    i = 0
    while not glfw.window_should_close(window):
        glfw.poll_events()
        renderer.clear()
        renderer.render_perspective(cam)
        renderer.render_axis()
        renderer.render_line(Vector3(0,0,0), Vector3(1,1,1))
        glfw.swap_buffers(window)
    glfw.terminate()

if __name__ == '__main__':
    main()
