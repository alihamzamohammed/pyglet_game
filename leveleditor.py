import pyglet
import cocos
from cocos.scene import *
from cocos.layer import *
from cocos.sprite import *
from cocos.tiles import *
from cocos.text import *
import xml.etree as et
from levels import levels
import logger

def loadLevel(lvl):
    pass

class LevelEditor(Scene):

    def __init__(self, level):
        super().__init__()
        self.levelArray = loadLevel(lvl)