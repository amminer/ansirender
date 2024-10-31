#pyright: basic
from ..sprite import Sprite

import random
from shutil import get_terminal_size
from time import sleep


class Field():
    def __init__(self):
        self.ncolumns = get_terminal_size().columns
        self.nlines = get_terminal_size().lines


    def print_at_position(self, text:str, x:int, y:int, ignore_whitespace:bool=False):
        output = '\n'.join([f"\033[{y+i};{x}H{line}" for i, line in enumerate(text.split('\n'))])
        if ignore_whitespace:
            output = output.replace(' ', '\033[1C')
        print(output, end='')


    def dvd(self, sprites: list[Sprite]):
        frames: list[str] = []
        positions: list[tuple[int,int]] = []
        directions: list[tuple[int,int]] = []
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
            # have to clean up each sprite before redrawing them in new positions
            for i, sprite in enumerate(sprites):
                position = positions[i]
                self.print_at_position(sprite.cleanup_frame, *position)
            # redraw sprites in new positions, determine next movements, sleep
            for i, sprite in enumerate(sprites):
                frame = frames[i]
                position = positions[i]
                h_direction, v_direction = directions[i]
                new_position = (position[0]+h_direction, position[1]+v_direction)
                self.print_at_position(frame, *new_position, ignore_whitespace=True)

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

            sleep(1/10)
