import os
import tkinter
from data_structure.mesh import Mesh


class tkScrollController:
    def __init__(self, slider, frametime):
        self.slider = slider
        self.frametime = frametime
        self.is_playing = False

    def next_frame(self):
        if self.is_playing:
            max = self.slider.cget("to")
            now = self.slider.get()
            next = (now + 1) % (max + 1)
            self.slider.set(next)
        self.slider.after(self.frametime, self.next_frame)

    def play(self):
        self.is_playing = True

    def pause(self):
        self.is_playing = False

    def tostart(self):
        self.slider.set(0)

    def toend(self):
        self.slider.set(self.slider.cget("to"))


class tkObjFileController:
    def __init__(self, label, filenames):
        self.idx = 0
        self.max_idx = len(filenames) - 1
        self.label = label
        self.filenames = filenames
        self.changed = True

    def next(self):
        if self.idx < self.max_idx:
            self.changed = True

            self.idx += 1
            self.label.text = self.filenames[self.idx]

    def prev(self):
        if self.idx > 0:
            self.changed = True
            self.idx -= 1
            self.label.text = self.filenames[self.idx]

    def end(self):
        self.changed = False


class tkInterFrameController:
    def __init__(self, renderframe, utilframe):
        self.renderframe = renderframe
        self.utilframe = utilframe


class tkInterObjFrameController(tkInterFrameController):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update_status(self):
        file_controller = self.utilframe.file_controller
        if file_controller.changed:
            print("sadfsadf")
            self.renderframe.set_mesh(
                Mesh.from_obj(
                    os.path.join(
                        self.utilframe.dirpath,
                        self.utilframe.filenames[self.utilframe.file_controller.idx],
                    )
                )
            )
            file_controller.end()
        self.renderframe.after(10, self.update_status)


class tkInterBvhFrameController(tkInterFrameController):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update_status(self):
        self.renderframe.frame_now = self.utilframe.aniframe_scroll.get()
        self.renderframe.selected_joint = self.utilframe.selected_joint.get()
        self.renderframe.after(10, self.update_status)
