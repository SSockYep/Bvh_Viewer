import numpy as np
import glfw
import wx

from OpenGL.GL import *
from OpenGL.GLU import *

from data_structure.math import *
from gl_render.renderer import *
from gl_render.camera import Camera
from gl_render.callback import Callback
from utility.bvh_loader import BvhLoader


def draw_points():
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glPointSize(10)
    glColor3ub(255, 255, 255)
    mat = np.eye(4)
    mat[1, 3] = 1.0
    mat[2, 3] = 1.0
    glPushMatrix()
    glBegin(GL_POINTS)
    glVertex3fv(np.array([1.0, 0.0, 0.0]))
    glEnd()
    # glTranslate(0.,1.,1.,)
    glMultTransposeMatrixf(mat)
    glPushMatrix()
    glBegin(GL_POINTS)
    glVertex3fv(np.array([1.0, 0.0, 0.0]))
    glEnd()
    glMultTransposeMatrixf(mat)
    glPushMatrix()
    glBegin(GL_POINTS)
    glVertex3fv(np.array([1.0, 0.0, 0.0]))
    glEnd()
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()


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
    callback = Callback(cam, window)
    glfw.set_mouse_button_callback(window, callback.mouse_callback)
    glfw.set_cursor_pos_callback(window, callback.cursor_callback)
    i = 0
    while not glfw.window_should_close(window):
        glfw.poll_events()
        renderer.clear()
        renderer.render_perspective(cam)
        renderer.render_global_axis()
        draw_points()
        glfw.swap_buffers(window)
    glfw.terminate()


if __name__ == "__main__":
    main()
