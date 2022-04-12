import tkinter


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


class tkInterFrameController:
    def __init__(self, renderframe, utilframe):
        self.renderframe = renderframe
        self.utilframe = utilframe

    def update_status(self):
        self.renderframe.frame_now = self.utilframe.aniframe_scroll.get()
        self.renderframe.after(10, self.update_status)
