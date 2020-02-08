import pyglet
import cocos
import os
from cocos import layer
from cocos.text import *
from cocos.actions import *
from cocos.sprite import *
from pyglet.window.key import symbol_string

import resources
import events
import cfg

x, y = director.window.width, director.window.height
reswidth, resheight = [int(res) for res in cfg.configuration["Core"]["defaultres"].split("x")]

titleLabel = cocos.text.Label(
    "Game Title",
    font_name=resources.font[1],
    font_size=50,
    anchor_y="top",
    anchor_x="center"
)

"""Main Menu Button. Sized and aligned to fit vertically on the game's main menu, as title buttons. Hardcoded to only use 4, but can be extended and used elsewhere."""
class MainMenuButton(layer.Layer):
    
    is_event_handler = True
    
    def __init__(self, label, eventName, buttonorder = 1):
        super().__init__()
        global x, y
        self.eventName = eventName
        self.label = label
        self.buttonorder = buttonorder
        self.bgImage = Sprite("menuButton.png") # Replace with proper resource pack image
        self.lbl = Label(self.label, anchor_x="center", anchor_y="center")
        
        self.x = x / 2
        self.TOPBTNPOS = 0.68
        self.y = y * (self.TOPBTNPOS - (0.16 * (buttonorder - 1)))
        
        self.width = self.bgImage.width
        self.height = self.bgImage.height
        
        self.add(self.bgImage, z = 0)
        self.add(self.lbl, z = 1)
        
        self.width_range = [int(self.x - (self.bgImage.width / 2)), int(self.x + (self.bgImage.width / 2))]
        self.height_range = [int(self.y - (self.bgImage.height / 2)), int(self.y + (self.bgImage.height / 2))]
        
        self.animate()

        self.schedule_interval(self.setWH, 1)
        self.resume_scheduler()

    def setWH(self, dt):
        x, y = director.window.width, director.window.height
        scalex = x / reswidth
        scaley = y / resheight
        self.width_range = [int((x / 2) - ((self.bgImage.width * scalex) / 2)), int((x / 2) + ((self.bgImage.width * scalex) / 2))]
        self.height_range = [int((y * (self.TOPBTNPOS - (0.16 * (self.buttonorder - 1)))) - ((self.bgImage.height * scaley) / 2)), int((y * (self.TOPBTNPOS - (0.16 * (self.buttonorder - 1)))) + ((self.bgImage.height * scaley) / 2))]

    def on_mouse_motion(self, x, y, dx, dy):
        if x in range(self.width_range[0], self.width_range[1]) and y in range(self.height_range[0], self.height_range[1]):
            self.bgImage.image = pyglet.resource.image("menuButtonHovered.png")
        else:
            self.bgImage.image = pyglet.resource.image("menuButton.png")

    def on_mouse_press(self, x, y, buttons, modifiers):
        if x in range(self.width_range[0], self.width_range[1]) and y in range(self.height_range[0], self.height_range[1]):
            self.eventName()
            self.bgImage.image = pyglet.resource.image("menuButtonClicked.png")
            self.lbl.element.color = (0, 0, 0, 255)

    def animate(self):
        mvx = self.x
        mvy = self.y
        # ODD
        if not self.buttonorder % 2 == 0:
            self.x = -self.width
            self.do(Delay(0.7) + AccelDeccel(MoveTo((mvx, mvy), 1.5)))
        # EVEN
        else:
            self.x = x + self.width
            self.do(Delay(0.7) + AccelDeccel(MoveTo((mvx, mvy), 1.5)))


"""Text Box. For inputting text."""
class TextBox(layer.Layer):

    is_event_handler = True

    def __init__(self, parent, selfx, selfy, default_text = "", charLimit = 1):
        super().__init__()
        self.px = parent.x
        self.py = parent.y
        self.x = selfx
        self.y = selfy
        self.charLimit = charLimit
        self.inputLabel = Label(default_text, font_size = 20, anchor_x = "center", anchor_y = "center", color=(0, 0, 0, 255))
        self.bgImage = Sprite("textBox.png")
        self.width = self.bgImage.width
        self.height = self.bgImage.height
        self.active = False
        self.add(self.bgImage)
        self.add(self.inputLabel)
        self.parentx = 0
        self.parenty = 0
        self.width_range = [int((self.parentx + self.x) - (self.bgImage.width / 2)), int((self.parentx + self.x) + (self.bgImage.width / 2))]
        self.height_range = [int((self.parenty + self.y) - (self.bgImage.height / 2)), int((self.parenty + self.y) + (self.bgImage.height / 2))]
        self.schedule_interval(self.setWH, 1)
        self.resume_scheduler()
        self.changed = False

    def setWH(self, dt):
        x, y = director.window.width, director.window.height
        scalex = x / reswidth
        scaley = y / resheight
        self.width_range = [int((self.parentx * scalex) + ((self.x * scalex) - (self.width * scalex) / 2)), int((self.parentx * scalex) + ((self.x * scalex) + (self.width * scalex) / 2))]
        self.height_range = [int((self.parenty * scaley) + ((self.y * scaley) - (self.height * scaley) / 2)), int((self.parenty * scaley) + ((self.y * scaley) + (self.height * scaley) / 2))]

    def on_mouse_motion(self, x, y, dx, dy):
        if not self.active:
            if x in range(self.width_range[0], self.width_range[1]) and y in range(self.height_range[0], self.height_range[1]):
                self.bgImage.image = pyglet.resource.image("textBoxHovered.png")
            else:
                self.bgImage.image = pyglet.resource.image("textBox.png")

    def on_mouse_press(self, x, y, buttons, modifiers):
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
                num = int(symbol_string(key)[-1])
                self.inputLabel.element.text = self.inputLabel.element.text + symbol_string(key)[-1]
                if len(self.inputLabel.element.text) > (self.charLimit - 1):
                    self.active = False
                    self.bgImage.image = pyglet.resource.image("textBox.png")
                    self.changed = True
        except ValueError:
            pass

    def get_text(self):
        return self.inputLabel.element.text


# TODO: Active and non-active checking
class sectionButton(layer.Layer):

    is_event_handler = True

    def __init__(self, label, eventName, active = False):
        super().__init__()
        global x, y

        self.eventName = eventName
        self.active = active

        self.bgImage = Sprite("settingsCategoryButton.png")
        self.lbl = Label(label, anchor_x="center", anchor_y="center")

        self.x = 0
        self.y = 0

        self.width_range = [int(self.x - (self.bgImage.width / 2)), int(self.x + (self.bgImage.width / 2))]
        self.height_range = [int(self.y - (self.bgImage.height / 2)), int(self.y + (self.bgImage.height / 2))]

        self.add(self.bgImage)
        self.add(self.lbl)

        self.schedule_interval(self.setWH, 1)
        self.resume_scheduler()
        
    def setWH(self, dt):
        x, y = director.window.width, director.window.height
        scalex = x / reswidth
        scaley = y / resheight
        self.width_range = [int((self.x * scalex) - ((self.bgImage.width * scalex) / 2)), int((self.x * scalex) + ((self.bgImage.width * scalex) / 2))]
        self.height_range = [int((self.y * scaley) - ((self.bgImage.height * scaley) / 2)), int((self.y * scaley) + ((self.bgImage.height * scaley) / 2))]

    def on_mouse_motion(self, x, y, dx, dy):
        if self.active:
            self.bgImage.image = pyglet.resource.image("settingsCategoryButtonClicked.png")
        elif x in range(self.width_range[0], self.width_range[1]) and y in range(self.height_range[0], self.height_range[1]):
            self.bgImage.image = pyglet.resource.image("settingsCategoryButtonHovered.png")
        else:
            self.bgImage.image = pyglet.resource.image("settingsCategoryButton.png")

    def on_mouse_press(self, x, y, buttons, modifiers):
        if x in range(self.width_range[0], self.width_range[1]) and y in range(self.height_range[0], self.height_range[1]):
            self.bgImage.image = pyglet.resource.image("settingsCategoryButtonClicked.png")
            self.active = True
            self.lbl.element.color = (0, 0, 0, 255)
            self.eventName()
