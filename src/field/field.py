#pyright: basic
from ..sprite import Sprite

import random
from shutil import get_terminal_size
from time import sleep
from typing import Callable


class Field():
    """
    implements internal utility _functions for programmatic rendering of sprites to the terminal,
    keeps state and exposes methods for procedurally rendering animations using those utilities.
    any method whose name doesn't begin with _ will be exposed to the CLI as an animation which must
    take an arbitrary list of Sprites. If sprites are preset for an animation, it should simply
    ignore the CLI's input sprites.
    all sprites must be redrawn at once for each frame in the animation to prevent destructive
    overlap. for animations where sprites are perfect quadrilaterals with no transparent regions,
    this rule is relaxed.
    performance scales linearly with the number of sprites being rendered.
    """
    def __init__(self):
        self.ncolumns = get_terminal_size().columns
        self.nlines = get_terminal_size().lines
        self.canvas = ''
        self.animations = [
            method for method in dir(Field)
            if callable(getattr(Field, method)) and not method.startswith('_')
        ]


    def _redraw_sprites(self, sprites: list[Sprite],
                        move_method: Callable = lambda _:None,
                        **move_kwargs) -> None:
        """
        :param sprites: all of the sprites that should be redrawn
        :param move_method: a function which must takes a Sprite as its first argument.
            may take any number of additional kwargs.
        :param move_kwargs: additional kwargs to pass to move_method

        for each sprite, passes the sprite to move_method,
        then prints the sprite's cleanup_frame at its prev_position.
        then, for each sprite again, prints the sprite at its position
        """
        self.canvas = ""
        for sprite in sprites:
            move_method(sprite, **move_kwargs)
            self._print_at_position(sprite.cleanup_frame, *sprite.prev_position)
        for sprite in sprites:
            self._print_at_position(sprite, *sprite.position, ignore_whitespace=True)
        print(self.canvas, end='')


    def _print_at_position(self, text: Sprite|str, x: int, y: int,
                           ignore_whitespace: bool = False) -> None:
        """
        prints a multiline string to the terminal at coords x, y from the origin using the usual
        computer-graphics axes, horizontal increasing to the right and vertical increasing downward

        :param ignore_whitespace: if True, replaces " " characters with ansi escapes which move the
            cursor one character to the right instead of literally printing the space character;
            prevents destructive overlap
        """
        output = '\n'.join([f"\033[{y+i};{x}H{line}" for i, line in enumerate(str(text).split('\n'))])
        if ignore_whitespace:
            output = output.replace(' ', '\033[1C')
        self.canvas += output
        #print(output, end='')


    #################
    # DVD ANIMATION #
    #################
    def dvd(self, sprites: list[Sprite]) -> None:
        """
        procedurally bounce sprite(s) around the terminal like the iconic "DVD VIDEO" screensaver
        """
        def __dvd_move(sprite):
            # determine next movement
            # If a sprite hits an edge, it bounces off
            if sprite.position[0]+sprite.width > self.ncolumns:
                h_direction = -1
            elif sprite.position[0] <= 1:
                h_direction = 1
            # else it maintains its current direction based on prev_position vs position
            elif sprite.position[0] > sprite.prev_position[0]:
                h_direction = 1
            else:
                h_direction = -1

            if sprite.position[1]+sprite.height > self.nlines:
                v_direction = -1
            elif sprite.position[1] <= 1:
                v_direction = 1
            elif sprite.position[1] > sprite.prev_position[1]:
                v_direction = 1
            else:
                v_direction = -1

            # apply movement
            new_position = (sprite.position[0]+h_direction, sprite.position[1]+v_direction)
            sprite.move(new_position)
            sprite.next_frame()

        # initialize sprites in random locations
        for sprite in sprites:
            position = (random.randint(0, self.ncolumns - sprite.width),
                        random.randint(0, self.nlines - sprite.height))
            sprite.position = position

            h_direction = random.choice((-1, 1))
            v_direction = random.choice((-1, 1))
            sprite.prev_position = (position[0]-h_direction, position[1]-v_direction)

        # run animation
        while True:
            self._redraw_sprites(sprites, __dvd_move)
            sleep(1/60)
