import tkinter
from pyopengltk import OpenGLFrame

from ui.tkutil import tkScrollController


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
        self.frame_now = 0

    def initgl(self):
        self.renderer.clear()
        self.renderer.render_perspective(self.cam)

    def redraw(self):
        self.renderer.clear()
        self.renderer.render_perspective(self.cam)
        self.renderer.render_global_axis()
        self.renderer.render_pose(
            self.skeleton, self.animation.get_pose(self.frame_now), scale=0.01
        )
        # self.renderer.render_pose() ## Get Pose idx


class tkUtilFrame(tkinter.Frame):
    def __init__(self, animation, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.grid()

        self.aniframe_scroll = tkinter.Scale(
            self, to=animation.frame - 1, orient=tkinter.HORIZONTAL
        )

        self.scroll_controller = tkScrollController(
            self.aniframe_scroll, int(animation.frame_time * 1000)
        )

        self.play_button = tkinter.Button(
            self,
            text="play",
            bitmap="@assets/ico_play.xbm",
            command=self.scroll_controller.play,
        )
        self.pause_button = tkinter.Button(
            self,
            text="pause",
            bitmap="@assets/ico_pause.xbm",
            command=self.scroll_controller.pause,
        )
        self.tostart_button = tkinter.Button(
            self,
            text="to start",
            bitmap="@assets/ico_tostart.xbm",
            command=self.scroll_controller.tostart,
        )
        self.toend_button = tkinter.Button(
            self,
            text="to end",
            bitmap="@assets/ico_toend.xbm",
            command=self.scroll_controller.toend,
        )

        self.columnconfigure(0, weight=5)
        self.columnconfigure(3, weight=5)

        self.tostart_button.grid(row=0, column=0, sticky=tkinter.E, padx=25, pady=5)
        self.play_button.grid(row=0, column=1, padx=3, pady=5)
        self.pause_button.grid(row=0, column=2, padx=3, pady=5)
        self.toend_button.grid(row=0, column=3, sticky=tkinter.W, padx=25, pady=5)
        self.aniframe_scroll.grid(
            row=1, column=0, columnspan=4, padx=5, pady=5, sticky=tkinter.EW
        )
