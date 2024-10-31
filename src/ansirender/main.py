#pyright: basic

import os
import sys
from ..sprite import Sprite
from ..field import Field


def main():

    # setup
    filepath = sys.argv[1]

    field = Field()
    size = (min(80, field.columns//2), min(80, field.lines//2))
    sprite = Sprite(filepath, size=size)


    # run
    os.system('clear')

    field.dvd(sprite)
