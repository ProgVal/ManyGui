# Curses magic...
from anygui.backends import *
__all__ = anygui.__all__

import anygui.backends.txtutils.scr_curses as scr_curses
scr_curses.scr_init()
import anygui.backends.txtutils.txtgui as txtgui
txtgui._support = scr_curses
x,y = scr_curses._xsize,scr_curses._ysize
txtgui._set_scale(x,y)
from anygui.backends.txtutils.txtgui import *
