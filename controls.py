import cocos
import pyglet
import events
from cocos import actions, layer, scene, text, sprite
from cocos.director import director
import scaling as sc
import cfg
import resources
from scroll import *
import elements
from pyglet.window import key as k

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
        self.add(self.title)
        blackLayer = layer.ColorLayer(0, 0, 0, 255)
        blackLayer.width = reswidth
        blackLayer.height = int(resheight * 0.35)
        blackLayer.x = 0
        blackLayer.y = int(resheight - (blackLayer.height / 2))
        self.add(blackLayer, z = -1)
        backButton = elements.mediumButton("BACK", events.mainmenuevents.onSettingsButtonClick)
        backButton.x = reswidth * 0.065
        backButton.y = resheight * 0.89
        self.add(backButton)       

        controlElements = []
        i = 0
        for control, value in cfg.configuration["Controls"]:
            lbl = text.Label(str(control).capitalize(), font_size=25, anchor_x="left", anchor_y="center", color=(255, 255, 255, 255))
            lbl.x = reswidth * 0.1
            lbl.y = 0.6 - (0.15 * i)
            txtBx = ControlTextBox(control)
            txtBx.x = reswidth * 0.9
            txtBx.y = 0.6 - (0.15 * i)
            self.scrollLayer.add(lbl)
            self.scrollLayer.add(txtBx)
            controlElements.append([lbl, txtBx])
            i += 1
        

        self.scrollManager.add(self.scrollLayer)
        self.scrollLayer.calculate()
        self.scrollManager.set_focus(reswidth / 2, resheight / 2)

        self.add(self.scrollManager)
        self.add(self.scrollBar)


class ControlTextBox(layer.Layer):

    is_event_handler = True

    def __init__(self, control):
        super().__init__()
        self.control = control
        self.inputLabel = elements.Label(cfg.configuration["Controls"][control], font_size = 15, anchor_x = "center", anchor_y = "center", color=(0, 0, 0, 255))
        self.bgImage = elements.Sprite("textBox.png")
        self.width = self.bgImage.width
        self.height = self.bgImage.height
        self.active = False
        self.add(self.bgImage)
        self.add(self.inputLabel)
        self.parentx = 0
        self.parenty = 0
        self.showing = self._showing = False
        self.width_range = [0, 0]
        self.height_range = [0, 0] 
        self.schedule_interval(self.setWH, 1)
        self.resume_scheduler()
        self.changed = False

    def setWH(self, dt):
        x, y = director.window.width, director.window.height
        nmin = sc.scale(int((self.parent.x + self.x) - (self.bgImage.width / 2)), int((self.parent.y + self.y) - (self.bgImage.height / 2)))
        nmax = sc.scale(int((self.parent.x + self.x) + (self.bgImage.width / 2)), int((self.parent.y + self.y) + (self.bgImage.height / 2)))
        self.width_range = [int(nmin[0]), int(nmax[0])]
        self.height_range = [int(nmin[1]), int(nmax[1])]


    def on_mouse_motion(self, x, y, dx, dy):
        if self.showing:
            if not self.active:
                if x in range(self.width_range[0], self.width_range[1]) and y in range(self.height_range[0], self.height_range[1]):
                    self.bgImage.image = pyglet.resource.image("textBoxHovered.png")
                else:
                    self.bgImage.image = pyglet.resource.image("textBox.png")

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self.showing:
            if x in range(self.width_range[0], self.width_range[1]) and y in range(self.height_range[0], self.height_range[1]):
                self.active = True
                self.bgImage.image = pyglet.resource.image("textBoxEntered.png")
                self.inputLabel.element.text = ""
            else:
                self.active = False
                self.bgImage.image = pyglet.resource.image("textBox.png")

    def on_key_press(self, key, modifiers):
        try:
            if self.active:
                val = k.symbol_string(key)
                self.inputLabel.element.text = val
                cfg.configuration["Controls"][self.control] = val
                self.active = False
                self.bgImage.image = pyglet.resource.image("textBox.png")
                self.changed = True
                return key
        except ValueError:
            pass

    def get_text(self):
        return self.inputLabel.element.text

    @property
    def showing(self):
        return self._showing

    @showing.setter
    def showing(self, value):
        self._showing = value

    def on_enter(self):
        super().on_enter()