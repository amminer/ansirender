#pyright: basic

import os
import signal
import sys
from ..sprite import Sprite
from ..field import Field


def sigint_handler(signum, frame):
        print('\033[?25h', end="")  # show cursor
        exit(0)
signal.signal(signal.SIGINT, sigint_handler)


def main():

    # setup
    print('\033[?25l', end="")  # hide cursor
    filepaths = [arg for arg in sys.argv[1:len(sys.argv)]]

    field = Field()
    size = (min(70, field.ncolumns//2), min(80, field.nlines//2))
    sprites = [Sprite(filepath, size=size) for filepath in filepaths]


    # run
    os.system('clear')

    field.dvd(sprites)
