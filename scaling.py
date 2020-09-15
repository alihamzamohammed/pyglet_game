import cocos
import pyglet
import cfg
from cocos.director import director

def scale(x, y):
    reswidth, resheight = [int(res) for res in cfg.configuration["Core"]["defaultres"].split("x")]
    winwidth, winheight = director.window.width, director.window.height
    newx, newy = 0, 0
    scaleFactor = min((winwidth / reswidth), (winheight / resheight))
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
    # This module and function is exclusively for caluclating scaled coordinates when the window is maximised or minimised. 
    # This function will return a scaled x and y coordinate pair from a x and y pair true to the original resolution
    

    # TODO: This all messes up when res is changed in settings, because settings res writes directly to config file, and config file 
    # TODO: settings are used to calculate current resolution. This can be remedied by not pulling res settings directly from config file.