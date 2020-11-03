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

# * cocos.tiles.load has a function names save_xml(), which saves the loaded folder to xml
# * Along with the ability to change the shown tile directly on the layer and have it reflect in the game, this can be used for level editor
