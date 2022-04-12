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

    glrender_frame = testframe(renderer, cam, root, width=800, height=600)
    glrender_frame.bind("<Motion>", callback.cursor_move_callback)
    glrender_frame.bind("<ButtonPress-1>", callback.lclick_callback)
    glrender_frame.bind("<ButtonPress-2>", callback.mclick_callback)
    glrender_frame.bind("<ButtonPress-3>", callback.rclick_callback)
    glrender_frame.bind("<ButtonRelease>", callback.release_callback)
    glrender_frame.grid(row=0)
    playutil_frame = tkinter.Frame(root, width=800)
    playutil_frame.grid(row=1, sticky=tkinter.EW)
    play_button = tkinter.Button(master=playutil_frame, text="play")
    print(play_button.master)
    play_button.grid(row=0, column=0, padx=5, pady=5, sticky=tkinter.E)
    pause_button = tkinter.Button(master=playutil_frame, text="pause")
    playutil_frame.columnconfigure(0, weight=5)
    pause_button.grid(row=0, column=1, padx=5, pady=5, sticky=tkinter.W)
    playutil_frame.columnconfigure(1, weight=5)
    anim_frame_slider = tkinter.Scale(
        master=playutil_frame, to=100, orient=tkinter.HORIZONTAL
    )
    anim_frame_slider.grid(row=1, columnspan=2, sticky=tkinter.EW)
    # playutil_frame.pack(fill=tkinter.X)

    glrender_frame.animate = 1
    glrender_frame.after(100, glrender_frame.printContext)
    glrender_frame.mainloop()


if __name__ == "__main__":
    main()
