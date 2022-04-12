import tkinter
from pyopengltk import OpenGLFrame


class tkRenderFrame(OpenGLFrame):
    def __init__(self, renderer, cam, callback, animation, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.renderer = renderer
        self.cam = cam
        self.bind("<Motion>", callback.cursor_move_callback)
        self.bind("<ButtonPress-1>", callback.lclick_callback)
        self.bind("<ButtonPress-2>", callback.mclick_callback)
        self.bind("<ButtonPress-3>", callback.rclick_callback)
        self.bind("<ButtonRelease>", callback.release_callback)
        self.skeleton = animation.skeleton
        self.animation = animation
        self.animate = 1

    def initgl(self):
        self.renderer.clear()
        self.renderer.render_perspective(self.cam)

    def redraw(self):
        self.renderer.clear()
        self.renderer.render_perspective(self.cam)
        self.renderer.render_global_axis()
        self.renderer.render_pose(self.skeleton, self.animation.get_pose(0), scale=0.01)
        # self.renderer.render_pose() ## Get Pose idx


class tkPlayFrame(tkinter.Frame):
    def __init__(self, anim_frames, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.grid()
        self.play_button = tkinter.Button(self, text="play")
        self.play_button.grid(row=0, column=0, sticky=tkinter.E)
        self.pause_button = tkinter.Button(self, text="pause")
        self.pause_button.grid(row=0, column=1, sticky=tkinter.W)
        self.aniframe_scroll = tkinter.Scale(
            self, to=anim_frames, orient=tkinter.HORIZONTAL
        )
        self.columnconfigure(0, weight=5)
        self.columnconfigure(1, weight=5)
        self.aniframe_scroll.grid(
            row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tkinter.EW
        )
