#pyright: basic

import argparse
import os
import signal


from ..sprite import Sprite
from ..field import Field


def sigint_handler(signum, frame):
    print('\033[?25h', end="")  # show cursor
    exit(0)
signal.signal(signal.SIGINT, sigint_handler)


def main():
    # setup
    parser = argparse.ArgumentParser(prog='ansirender')
    parser.add_argument('-a', '--animation', required=True, action='store', type=str)
    parser.add_argument('-f', '--files', required=True, action='store', type=str, nargs='*')
    args = parser.parse_args()

    field = Field()
    size = (field.ncolumns//2, field.nlines//2)
    print(size)
    #exit()
    sprites = [Sprite(filepath, size=size) for filepath in args.files]

    # run
    print('\033[?25l', end="")  # hide cursor
    try:
        try:
            animation = getattr(field, args.animation)
            os.system('clear')
            animation(sprites)
        except AttributeError as e:
            raise ValueError(f'{args.animation} is not a valid animation, must be one of {field.animations}')
    except Exception as e:
        print(e)
        exit(1)
    finally:
        print('\033[?25h', end="")  # show cursor


if __name__ == '__main__':
    main()
