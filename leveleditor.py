import pyglet
import cocos
from cocos.scene import *
from cocos.layer import *
from cocos.sprite import *
from cocos.tiles import *
from cocos.text import *
import xml.etree.ElementTree as et
from levels import levels
import logger

def loadLevel(lvl):
    lvl = levels.Level()
    if not isinstance(lvl, levels.Level):
        return None
    levelArray = []
    for column in lvl.data.getroot():
        for rows in column:
            pass

class LevelEditor(Scene):

    def __init__(self, level):
        super().__init__()
        self.levelArray = loadLevel(level)