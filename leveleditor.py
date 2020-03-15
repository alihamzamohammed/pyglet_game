import pyglet
import cocos
from cocos.scene import *
from cocos.layer import *
from cocos.sprite import *
from cocos.tiles import *
from cocos.text import *
import xml.etree as et
import logger


def loadLevel(lvlPath):
    try:
        with open(lvlPath) as lvl:
            xmllvl = et.ElementTree.parse(lvl)


class LevelEditor(Scene):

    def __init__(self, level):
        super().__init__()
        loadLevel(level)