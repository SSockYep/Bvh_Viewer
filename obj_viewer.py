from tkinter import messagebox
import numpy as np
import tkinter
from tkinter import filedialog
import os

from OpenGL.GL import *
from OpenGL.GLU import *

from data_structure.math import *
from data_structure.mesh import Mesh
from gl_render.renderer import *
from gl_render.camera import Camera
from gl_render.callback import Callback
from ui.tkutil import tkInterBvhFrameController, tkInterObjFrameController
from utility.bvh_loader import BvhLoader
from ui.tkframe import (
    tkAnimRenderFrame,
    tkAnimUtilFrame,
    tkObjRenderFrame,
    tkObjUtilFrame,
)

import pdb


def main():
    renderer = Renderer(scale=1)
    cam = Camera()
    root = tkinter.Tk()
    callback = Callback(cam, root)

    dir_path = filedialog.askdirectory(
        parent=root, initialdir=".", title="select a directory"
    )
    filenames = os.listdir(dir_path)
    for filename in os.listdir(dir_path):
        if filename[-4:] not in [".obj", ".OBJ"]:
            filenames.remove(filename)

    if len(filenames) == 0:
        messagebox.showerror("no obj", "there is no obj file in directory")
        return
    filenames = sorted(filenames)

    root.grid()
    render_frame = tkObjRenderFrame(
        Mesh.from_obj(os.path.join(dir_path, filenames[0])),
        root,
        renderer,
        cam,
        callback,
        width=800,
        height=600,
    )
    util_frame = tkObjUtilFrame(dir_path, filenames, root)
    render_frame.grid(row=0)
    util_frame.grid(row=1)
    interframe_controller = tkInterObjFrameController(render_frame, util_frame)
    render_frame.after(10, interframe_controller.update_status)

    root.mainloop()


if __name__ == "__main__":
    main()
