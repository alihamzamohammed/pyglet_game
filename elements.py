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
import scaling as sc

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

    def __init__(self, label, eventName, buttonorder = 1, animate=True):
        super().__init__()
        global x, y
        self.eventName = eventName
        self.label = label
        self.buttonorder = buttonorder
        self.bgImage = Sprite("menuButton.png") # Replace with proper resource pack image
        self.lbl = Label(self.label, anchor_x="center", anchor_y="center", dpi=110)

        self.x = x / 2
        self.TOPBTNPOS = 0.68
        self.y = y * (self.TOPBTNPOS - (0.16 * (buttonorder - 1)))

        self.width = self.bgImage.width
        self.height = self.bgImage.height

        self.add(self.bgImage, z = 0)
        self.add(self.lbl, z = 1)

        self.width_range = [int(self.x - (self.bgImage.width / 2)), int(self.x + (self.bgImage.width / 2))]
        self.height_range = [int(self.y - (self.bgImage.height / 2)), int(self.y + (self.bgImage.height / 2))]

        if animate:
            self.animate()

        self.schedule_interval(self.setWH, 1)
        self.resume_scheduler()

    def setWH(self, dt):
        x, y = director.window.width, director.window.height
        nmin = sc.scale(int(self.x - (self.bgImage.width / 2)), int(self.y - (self.bgImage.height / 2)))
        nmax = sc.scale(int(self.x + (self.bgImage.width / 2)), int(self.y + (self.bgImage.height / 2)))
        self.width_range = [int(nmin[0]), int(nmax[0])]
        self.height_range = [int(nmin[1]), int(nmax[1])]


    def on_mouse_motion(self, x, y, dx, dy):
        if x in range(self.width_range[0], self.width_range[1]) and y in range(self.height_range[0], self.height_range[1]):
            self.bgImage.image = pyglet.resource.image("menuButtonHovered.png")
            self.lbl.element.color = (255, 255, 255, (self.lbl.element.color[-1]))
        else:
            self.bgImage.image = pyglet.resource.image("menuButton.png")
            self.lbl.element.color = (255, 255, 255, (self.lbl.element.color[-1]))

    def on_mouse_press(self, x, y, buttons, modifiers):
        if x in range(self.width_range[0], self.width_range[1]) and y in range(self.height_range[0], self.height_range[1]):
            self.eventName()
            self.bgImage.image = pyglet.resource.image("menuButtonClicked.png")
            self.lbl.element.color = (0, 0, 0, (self.lbl.element.color[-1]))

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
        nmin = sc.scale(int((self.parentx + self.x) - (self.bgImage.width / 2)), int((self.parenty + self.y) - (self.bgImage.height / 2)))
        nmax = sc.scale(int((self.parentx + self.x) + (self.bgImage.width / 2)), int((self.parenty + self.y) + (self.bgImage.height / 2)))
        self.width_range = [int(nmin[0]), int(nmax[0])]
        self.height_range = [int(nmin[1]), int(nmax[1])]


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
"""Section Button. For activating a section of a page"""
class sectionButton(layer.Layer):

    is_event_handler = True

    def __init__(self, label, eventName, active = False):
        super().__init__()
        global x, y

        self.eventName = eventName
        self.active = active

        self.bgImage = Sprite("settingsCategoryButton.png")
        self.lbl = Label(label, anchor_x="center", anchor_y="center", dpi=110)

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
        nmin = sc.scale(int(self.x - (self.bgImage.width / 2)), int(self.y - (self.bgImage.height / 2)))
        nmax = sc.scale(int(self.x + (self.bgImage.width / 2)), int(self.y + (self.bgImage.height / 2)))
        self.width_range = [int(nmin[0]), int(nmax[0])]
        self.height_range = [int(nmin[1]), int(nmax[1])]

    def on_mouse_motion(self, x, y, dx, dy):
        if self.active:
            self.bgImage.image = pyglet.resource.image("settingsCategoryButtonClicked.png")
            self.lbl.element.color = (0, 0, 0, 255)
        elif x in range(self.width_range[0], self.width_range[1]) and y in range(self.height_range[0], self.height_range[1]):
            self.bgImage.image = pyglet.resource.image("settingsCategoryButtonHovered.png")
            self.lbl.element.color = (255, 255, 255, 255)
        else:
            self.bgImage.image = pyglet.resource.image("settingsCategoryButton.png")
            self.lbl.element.color = (255, 255, 255, 255)

    def on_mouse_press(self, x, y, buttons, modifiers):
        if x in range(self.width_range[0], self.width_range[1]) and y in range(self.height_range[0], self.height_range[1]):
            self.bgImage.image = pyglet.resource.image("settingsCategoryButtonClicked.png")
            self.active = True
            self.lbl.element.color = (0, 0, 0, 255)
            self.eventName()


"""Toggle Button. For toggling a setting on or off. Can alter a value in a dictionary and run a command simultaneously."""
class ToggleButton(layer.Layer):

    is_event_handler = True

    def __init__(self, parent, selfx, selfy, configDict, section, option, command = None):
        super().__init__()
        global x, y
        self.px = parent.x
        self.py = parent.y
        pwidth = parent.width
        pheight = parent.height
        self.command = command
        self.configDict = configDict
        self.section = section
        self.option = option
        self.lbl = Label("YES", anchor_x="center", anchor_y="center", dpi=105)
        self.bgImage = Sprite("toggleButton.png")
        self.active = True if self.configDict[self.section][self.option] == "True" else False
        self.changed = False
        if self.active:
            self.bgImage.image = pyglet.resource.image("toggledButton.png")
            self.lbl.element.text = "YES"
        else:
            self.bgImage.image = pyglet.resource.image("toggleButton.png")
            self.lbl.element.text = "NO"
        self.width = self.bgImage.width
        self.height = self.bgImage.height
        self.x = pwidth * selfx
        self.y = pheight * selfy
        self.lbl.x = 0
        self.lbl.y = 0
        self.add(self.bgImage)
        self.add(self.lbl)
        self.width_range = [int(self.px + (self.x - (self.width / 2))), int(self.px + (self.x + (self.width / 2)))]
        self.height_range = [int(self.py + (self.y - (self.height / 2))), int(self.py + (self.y + (self.height / 2)))]
        self.schedule_interval(self.setWH, 1)
        self.resume_scheduler()

    def setWH(self, dt):
        x, y = director.window.width, director.window.height
        nmin = sc.scale(int(self.px + (self.x - (self.width / 2))), int(self.py + (self.y - (self.height / 2))))
        nmax = sc.scale(int(self.px + (self.x + (self.width / 2))), int(self.py + (self.y + (self.height / 2))))
        self.width_range = [int(nmin[0]), int(nmax[0])]
        self.height_range = [int(nmin[1]), int(nmax[1])]

    def on_mouse_motion(self, x, y, dx, dy):
        if x in range(self.width_range[0], self.width_range[1]) and y in range(self.height_range[0], self.height_range[1]):
            if self.active:
                self.bgImage.image = pyglet.resource.image("toggledButtonHovered.png")
            else:
                self.bgImage.image = pyglet.resource.image("toggleButtonHovered.png")
        else:
            if self.active:
                self.bgImage.image = pyglet.resource.image("toggledButton.png")
            else:
                self.bgImage.image = pyglet.resource.image("toggleButton.png")

    def on_mouse_press(self, x, y, buttons, modifiers):
        if x in range(self.width_range[0], self.width_range[1]) and y in range(self.height_range[0], self.height_range[1]):
            self.active = not self.active
            self.changed = True
            self.configDict[self.section][self.option] = str(self.active)
            if callable(self.command):
                self.command(self.active)
            if self.active:
                self.bgImage.image = pyglet.resource.image("toggledButtonClicked.png")
                self.lbl.element.text = "YES"
            else:
                self.bgImage.image = pyglet.resource.image("toggleButtonClicked.png")
                self.lbl.element.text = "NO"


