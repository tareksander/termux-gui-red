from __future__ import annotations

import sys

try:
    import termuxgui.oo as tgo
except ModuleNotFoundError:
    sys.exit("termuxgui module not found. Please install the Termux:GUI python bindings: https://github.com/tareksander/termux-gui-python-bindings")

try:
    import praw
except ModuleNotFoundError:
    sys.exit("praw module not found. Please install praw with pip install praw")

from activity import Activity


with tgo.Connection() as c:
    c.launch(Activity)
    c.event_loop()


