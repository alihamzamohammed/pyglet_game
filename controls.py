import cocos
import pyglet
import events
from cocos import actions, layer, scene, text, sprite
from cocos.director import director
import scaling as sc
import cfg
import resources
from scroll import *

reswidth, resheight = [int(res) for res in cfg.resolution.split("x")]

class Controls(scene.Scene):
    
    def __init__(self, *children):
        super().__init__(*children)
        self.scrollManager = layer.ScrollingManager()
        self.scrollBar = ScrollBar(self.scrollManager)
        self.scrollLayer = ScrollLayer(reswidth/2, resheight, reswidth, resheight, self.scrollBar)
        
        self.scrollLayer.x = 0
        self.scrollLayer.y = 0

        self.scrollBar.x = reswidth - (self.scrollBar.width / 2)
        self.scrollBar.y = (resheight - (resheight * 0.02)) - (self.scrollBar.img.height / 2)

        self.title = text.Label("Controls", font_name=resources.font[1], font_size=50, anchor_y="top", anchor_x="center")
        self.title.x = reswidth / 2
        self.title.y = resheight * 0.85 
        self.scrollLayer.add(self.title)
        for i in range(-1, 20):
            sp = sprite.Sprite("smallButton.png")
            if i == -1 or i == 19:
                sp.image = pyglet.resource.image("smallButtonHovered.png")
            sp.x = reswidth / 2
            sp.y = (resheight * 0.5) * -i
            self.scrollLayer.add(sp)


        self.scrollManager.add(self.scrollLayer)
        self.scrollLayer.calculate()
        self.scrollManager.set_focus(reswidth / 2, resheight / 2)

        self.add(self.scrollManager)
        self.add(self.scrollBar)