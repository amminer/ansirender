#pyright: basic
from ..config import ansi_escape_pattern

from ansifier import ansify  # pyright: ignore


class Sprite():
    """
    Converts an image or video file into a list of ansi-escaped strings (one per input frame),
    keeps state and exposes methods for:
     * positioning the image in 2d space
     * selecting the "current" frame to be used upon rendering
     * rendering and de-rendering the image to and from a terminal
    """
    def __init__(self, filepath: str,
                 size: tuple[int, int] = (20, 20)):
        self._index = 0
        self.frames = ansify(filepath, width=size[0], height=size[1], chars='█▓▒░ ')
        self.nframes = len(self.frames)

        frame0_lines = [ansi_escape_pattern.sub('', line)
                        for line in self.frames[0].split('\n')]
        self.height = len(frame0_lines)
        self.width = len(frame0_lines[0])
        self.cleanup_frame = '\n'.join([
            (' ' * len(ansi_escape_pattern.sub('', line))) for line in self.frames[0].split('\n')])

        self.position: tuple[int, int] = (0, 0)
        self.prev_position: tuple[int, int] = (0, 0)


    def __str__(self):
        return self.frames[self._index]


    def next_frame(self) -> str:
        """
        progress the current frame to the next frame in self.frames
        when called at last frame, loops back to first frame
        :return: str, the current frame BEFORE the increment
        """
        ret = str(self)
        self._index = (self._index + 1) % self.nframes
        return ret


    def reset_frame(self) -> None:
        """ reset the current frame to the first frame """
        self._index = 0


    def move(self, new_position: tuple[int, int]) -> None:
        """ update internal prev_position & position state based on new_position """
        self.prev_position = self.position
        self.position = new_position
