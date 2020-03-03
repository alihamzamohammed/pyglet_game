import pyglet
import cocos
from cocos.scene import *
from cocos.layer import *
from cocos.sprite import *
from cocos.tiles import *
from cocos.text import *
import xml.etree as et

class LevelEditor(Scene):

    def __init__(self):
        super().__init__()