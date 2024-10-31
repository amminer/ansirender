#pyright: basic

from ..sprite import Sprite

from shutil import get_terminal_size
from time import sleep


class Field():
    def __init__(self):
        self.columns = get_terminal_size().columns
        self.lines = get_terminal_size().lines


    def print_at_position(self, text, x, y):
        output = '\n'.join([f"\033[{y+i};{x}H{line}" for i, line in enumerate(text.split('\n'))])
        print(output, end='')


    def dvd(self, sprite: Sprite):
        frame = sprite.animate()
        position = (0, 0)
        h_direction = 1
        v_direction = 1
        while True:
            new_position = (position[0]+h_direction, position[1]+v_direction)
            self.print_at_position(sprite.cleanup_frame, *position)
            self.print_at_position(frame, *new_position)
            position = new_position

            if position[0]+sprite.width > self.columns:
                h_direction = -1
            elif position[0] <= 1:
                h_direction = 1
            if position[1]+sprite.height > self.lines:
                v_direction = -1
            elif position[1] <= 1:
                v_direction = 1

            frame = sprite.animate()
            sleep(1/20)
