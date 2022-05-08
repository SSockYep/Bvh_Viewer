import tkinter
import numpy as np
from pyopengltk import OpenGLFrame

from ui.tkutil import tkScrollController


class tkRenderFrame(OpenGLFrame):
    def __init__(
        self, renderer, cam, callback, animation, master, pose=None, *args, **kwargs
    ):
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
        self.selected_joint = "None"
        self.pose = pose

    def initgl(self):
        self.renderer.clear()
        self.renderer.render_perspective(self.cam)

    def redraw(self):
        pose = self.animation.get_pose(self.frame_now)
        self.renderer.clear()
        self.renderer.render_perspective(self.cam)
        self.renderer.render_global_axis()
        self.renderer.render_pose(self.skeleton, pose)
        if self.pose:
            self.renderer.render_pose(
                self.skeleton, self.pose, color=np.array([255, 0, 255], dtype=np.ubyte)
            )
        if self.selected_joint != "None":
            joint_pos = self.animation.get_joint_pos_on_frame(
                self.selected_joint, self.frame_now
            )
            self.renderer.render_point(joint_pos)
            if self.frame_now > 0:
                pos, vel = self.animation.get_joint_velocity(
                    self.selected_joint, self.frame_now
                )
                self.renderer.render_line(pos, vel, np.array([255, 255, 0], np.ubyte))
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
        option_list = ["None"]
        for i in range(animation.skeleton.num_nodes()):
            node = animation.skeleton.get_node_by_index(i)
            option_list.append(node.get_name())
        self.selected_joint = tkinter.StringVar()
        self.selected_joint.set(option_list[0])
        self.joint_option = tkinter.OptionMenu(self, self.selected_joint, *option_list)
        self.joint_option.configure(width=35)
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
        self.option_label = tkinter.Label(self, text="select joint: ")

        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, weight=3)

        self.option_label.grid(row=0, column=0, columnspan=2, sticky=tkinter.E, pady=10)
        self.joint_option.grid(
            row=0, column=2, columnspan=2, sticky=tkinter.EW, pady=10, padx=25
        )

        self.tostart_button.grid(row=1, column=0, sticky=tkinter.W, padx=25, pady=5)
        self.play_button.grid(row=1, column=1, padx=3, pady=5, sticky=tkinter.E)
        self.pause_button.grid(row=1, column=2, padx=3, pady=5, sticky=tkinter.W)
        self.toend_button.grid(row=1, column=3, sticky=tkinter.E, padx=25, pady=5)

        self.aniframe_scroll.grid(
            row=2, column=0, columnspan=4, padx=50, pady=5, sticky=tkinter.EW
        )
