import re


ansi_escape_pattern = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
