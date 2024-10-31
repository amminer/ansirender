#pyright: basic

from ..config import ansi_escape_pattern

from ansifier import ansify


class Sprite():
    def __init__(self, filepath, size=(20, 20)):
        self.index = 0
        self.frames = ansify(filepath, width=size[0], height=size[1])
        self.nframes = len(self.frames)
        frame0_lines = [ansi_escape_pattern.sub('', line)
                        for line in self.frames[0].split('\n')]

        self.height = len(frame0_lines)
        self.width = len(frame0_lines[0])
        self.cleanup_frame = '\n'.join([
            (' ' * len(ansi_escape_pattern.sub('', line))) for line in self.frames[0].split('\n')])

    def __str__(self):
        return self.frames[self.index]

    def animate(self):
        ret = str(self)
        self.index = (self.index + 1) % self.nframes
        return ret

    def reset_animation(self):
        self.index = 0
