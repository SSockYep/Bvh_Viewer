import numpy as np
import tkinter
from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame

from data_structure.math import *
from gl_render.renderer import *
from gl_render.camera import Camera
from gl_render.callback import Callback
from utility.bvh_loader import BvhLoader


class testframe(OpenGLFrame):
    def __init__(self, renderer, cam, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.renderer = renderer
        self.cam = cam

    def initgl(self):
        self.renderer.clear()
        self.renderer.render_perspective(self.cam)

    def redraw(self):
        self.renderer.clear()
        self.renderer.render_perspective(self.cam)
        self.renderer.render_global_axis()
        self.draw_points()

    def draw_points(self):
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
    renderer = Renderer()
    cam = Camera()
    root = tkinter.Tk()
    callback = Callback(cam, root)
    root.bind("<Motion>", callback.cursor_move_callback)
    root.bind("<ButtonPress-1>", callback.lclick_callback)
    root.bind("<ButtonPress-2>", callback.mclick_callback)
    root.bind("<ButtonPress-3>", callback.rclick_callback)
    root.bind("<ButtonRelease>", callback.release_callback)
    app = testframe(renderer, cam, root, width=800, height=600)
    app.pack(fill=tkinter.BOTH, expand=tkinter.YES)
    app.animate = 1
    app.after(100, app.printContext)
    app.mainloop()


if __name__ == "__main__":
    main()
