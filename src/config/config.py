import re


ansi_escape_pattern = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
cell_pattern = re.compile(r'(\x9B|\x1B\[38;2;\d+;\d+;\d+m)')
