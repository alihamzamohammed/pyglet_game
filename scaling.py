import cocos
import pyglet
import cfg
from cocos.director import director

def sc(x, y):
    reswidth, resheight = [int(res) for res in cfg.configuration["Core"]["defaultres"].split("x")]
    winwidth, winheight = director.window.width, director.window.height
    newx, newy = 0, 0
    scaleFactor = min((reswidth / winwidth), (resheight / winheight))
    if (reswidth / winwidth) == scaleFactor:
        newx = x * scaleFactor
    else:
        excess = (winwidth - (reswidth * scaleFactor)) / 2
        newx = excess + (x * scaleFactor)
    if (resheight / winheight) == scaleFactor:
        newy = y * scaleFactor
    else:
        excess = (winheight - (resheight * scaleFactor)) / 2
        newy = excess + (y * scaleFactor)
    return newx, newy
    # TODO: This module and function is exclusively for caluclating scaled coordinates when the window is maximised or minimised. 
    # TODO: This function will return a scaled x and y coordinate pair from a x and y pair true to the original resolution
    