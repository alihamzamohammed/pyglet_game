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
# * items.itempacks now has loaded resource and tile objects for each item in an item pack. This can be used to directly change data in the tileset.
# * However, care must be taken to find if the item is not in the level's required, that is it added there, otherwise the level will not work at all
# * This can be done by finding the res class in the item pack's item_res dictionary, and adding it to the level's required list as a tuple
# * This check can be done when an item is changed on the level 

# ? Find out how to refresh the cocos level renderer when a new tile is placed, as it caches the old tile until it goes off viewport