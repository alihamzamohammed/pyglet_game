import cocos
import pyglet
import events
from cocos import actions, layer, scene, text, sprite
from cocos.director import director
import scaling as sc
import cfg
import resources
from scroll import *

rx, ry = director.window.width, director.window.height
reswidth, resheight = [int(res) for res in cfg.resolution.split("x")]

class testScroller(scene.Scene):
    
    def __init__(self, *children):
        super().__init__(*children)
        parentLayer = ParentLayer()
        self.add(parentLayer)
        
        