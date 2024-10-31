#pyright: basic

import os
import sys
from ..sprite import Sprite
from ..field import Field


def main():

    # setup
    filepaths = [arg for arg in sys.argv[1:len(sys.argv)]]

    field = Field()
    size = (min(80, field.ncolumns//2), min(80, field.nlines//2))
    sprites = [Sprite(filepath, size=size) for filepath in filepaths]


    # run
    os.system('clear')

    field.dvd(sprites)
