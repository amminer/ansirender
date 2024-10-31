#pyright: basic
from ..sprite import Sprite

import random
from shutil import get_terminal_size
from time import sleep


class Field():
    def __init__(self):
        self.ncolumns = get_terminal_size().columns
        self.nlines = get_terminal_size().lines


    def print_at_position(self, text:Sprite|str, x:int, y:int, ignore_whitespace:bool=False):
        output = '\n'.join([f"\033[{y+i};{x}H{line}" for i, line in enumerate(str(text).split('\n'))])
        if ignore_whitespace:
            output = output.replace(' ', '\033[1C')
        print(output, end='')


    def dvd(self, sprites: list[Sprite]):
        directions: list[tuple[int,int]] = []
        for sprite in sprites:
            position = (random.randint(0, self.ncolumns - sprite.width),
                        random.randint(0, self.nlines - sprite.height))
            sprite.position = position

            h_direction = random.choice((-1, 1))
            v_direction = random.choice((-1, 1))
            directions.append((h_direction, v_direction))

        while True:
            # clean up all sprites before redrawing the field
            for i, sprite in enumerate(sprites):
                self.print_at_position(sprite.cleanup_frame, *sprite.position)
            # redraw all sprites, determine next movements, sleep
            for i, sprite in enumerate(sprites):
                h_direction, v_direction = directions[i]
                new_position = (sprite.position[0]+h_direction, sprite.position[1]+v_direction)
                sprite.move(new_position)
                self.print_at_position(sprite, *sprite.position, ignore_whitespace=True)

                if sprite.position[0]+sprite.width > self.ncolumns:
                    h_direction = -1
                elif sprite.position[0] <= 1:
                    h_direction = 1
                if sprite.position[1]+sprite.height > self.nlines:
                    v_direction = -1
                elif sprite.position[1] <= 1:
                    v_direction = 1

                sprite.animate()
                directions[i] = (h_direction, v_direction)

            sleep(1/5)
