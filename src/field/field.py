#pyright: basic

from ..sprite import Sprite

import random
from shutil import get_terminal_size
from time import sleep


class Field():
    def __init__(self):
        self.ncolumns = get_terminal_size().columns
        self.nlines = get_terminal_size().lines


    def print_at_position(self, text, x, y):
        output = '\n'.join([f"\033[{y+i};{x}H{line}" for i, line in enumerate(text.split('\n'))])
        print(output, end='')


    def dvd(self, sprites: list[Sprite]):
        frames = []
        positions = []
        directions = []
        for sprite in sprites:
            frame = sprite.animate()
            frames.append(frame)

            position = (random.randint(0, self.ncolumns - sprite.width),
                        random.randint(0, self.nlines - sprite.height))
            positions.append(position)

            h_direction = random.choice((-1, 1))
            v_direction = random.choice((-1, 1))
            directions.append((h_direction, v_direction))

        while True:
            for i, sprite in enumerate(sprites):
                frame = frames[i]
                position = positions[i]
                h_direction, v_direction = directions[i]

                new_position = (position[0]+h_direction, position[1]+v_direction)
                self.print_at_position(sprite.cleanup_frame, *position)
                self.print_at_position(frame, *new_position)

                if new_position[0]+sprite.width > self.ncolumns:
                    h_direction = -1
                elif new_position[0] <= 1:
                    h_direction = 1
                if new_position[1]+sprite.height > self.nlines:
                    v_direction = -1
                elif new_position[1] <= 1:
                    v_direction = 1

                frames[i] = sprite.animate()
                positions[i] = new_position
                directions[i] = (h_direction, v_direction)

            sleep(1/20)
