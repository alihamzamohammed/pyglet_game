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
reswidth, resheight = [int(res) for res in cfg.resolution.split("x")]

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


"""Medium button. Same as small button, but can contain more text"""
class mediumButton(layer.Layer):

    is_event_handler = True

    def __init__(self, label, eventName, active = False, *args, **kwargs):
        super().__init__()
        global x, y

        self.eventName = eventName
        self.active = active
        if "eventparam" in kwargs:
            self.eventparam = kwargs["eventparam"]

        self.bgImage = Sprite("mediumButton.png")
        self.lbl = Label(label, anchor_x="center", anchor_y="center", dpi=110, font_size=16)

        self.x = 0
        self.y = 0
        self.px = 0
        self.py = 0

        self.width_range = [int((self.px + self.x) - (self.bgImage.width / 2)), int((self.px + self.x) + (self.bgImage.width / 2))]
        self.height_range = [int((self.py + self.y) - (self.bgImage.height / 2)), int((self.py + self.y) + (self.bgImage.width / 2))]

        self.add(self.bgImage)
        self.add(self.lbl)

        self.hide(0.01)
        self.showing = False

        self.schedule_interval(self.setWH, 1)
        self.resume_scheduler()

    def setWH(self, dt):
        x, y = director.window.width, director.window.height
        nmin = sc.scale(int((self.px + self.x) - (self.bgImage.width / 2)), int((self.py + self.y) - (self.bgImage.height / 2)))
        nmax = sc.scale(int((self.px + self.x) + (self.bgImage.width / 2)), int((self.py + self.y) + (self.bgImage.width / 2)))
        self.width_range = [int(nmin[0]), int(nmax[0])]
        self.height_range = [int(nmin[1]), int(nmax[1])]

    def on_mouse_motion(self, x, y, dx, dy):
        if self.showing:
            if self.active:
                self.bgImage.image = pyglet.resource.image("mediumButtonClicked.png")
                self.lbl.element.color = (0, 0, 0, 255)
            elif x in range(self.width_range[0], self.width_range[1]) and y in range(self.height_range[0], self.height_range[1]):
                self.bgImage.image = pyglet.resource.image("mediumButtonHovered.png")
                self.lbl.element.color = (255, 255, 255, 255)
            else:
                self.bgImage.image = pyglet.resource.image("mediumButton.png")
                self.lbl.element.color = (255, 255, 255, 255)

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self.showing:
            if x in range(self.width_range[0], self.width_range[1]) and y in range(self.height_range[0], self.height_range[1]):
                self.bgImage.image = pyglet.resource.image("mediumButtonClicked.png")
                self.active = True
                self.lbl.element.color = (0, 0, 0, 255)
                if hasattr(self, "eventparam"):
                    self.eventName(self.eventparam)
                else:
                    self.eventName() 
                self.active = False
    
    def show(self, interval = 0.5):
        for child in self.get_children():
            child.do(FadeIn(interval))
        self.showing = True

    def hide(self, interval = 0.5):
        for child in self.get_children():
            child.do(FadeOut(interval))
        self.showing = False


"""Small button. A button for placing in small spaces, or to activate non-crucial functions"""
class smallButton(layer.Layer):

    is_event_handler = True

    def __init__(self, label, eventName, active = False, *args, **kwargs):
        super().__init__()
        global x, y

        self.eventName = eventName
        self.active = active
        if "eventparam" in kwargs:
            self.eventparam = kwargs["eventparam"]

        self.bgImage = Sprite("smallButton.png")
        self.lbl = Label(label, anchor_x="center", anchor_y="center", dpi=110, font_size=16)

        self.x = 0
        self.y = 0
        self.px = 0
        self.py = 0

        self.width_range = [int((self.px + self.x) - (self.bgImage.width / 2)), int((self.px + self.x) + (self.bgImage.width / 2))]
        self.height_range = [int((self.py + self.y) - (self.bgImage.height / 2)), int((self.py + self.y) + (self.bgImage.width / 2))]

        self.add(self.bgImage)
        self.add(self.lbl)

        self.hide(0.01)
        self.showing = False

        self.schedule_interval(self.setWH, 1)
        self.resume_scheduler()

    def setWH(self, dt):
        x, y = director.window.width, director.window.height
        nmin = sc.scale(int((self.px + self.x) - (self.bgImage.width / 2)), int((self.py + self.y) - (self.bgImage.height / 2)))
        nmax = sc.scale(int((self.px + self.x) + (self.bgImage.width / 2)), int((self.py + self.y) + (self.bgImage.width / 2)))
        self.width_range = [int(nmin[0]), int(nmax[0])]
        self.height_range = [int(nmin[1]), int(nmax[1])]

    def on_mouse_motion(self, x, y, dx, dy):
        if self.showing:
            if self.active:
                self.bgImage.image = pyglet.resource.image("smallButtonClicked.png")
                self.lbl.element.color = (0, 0, 0, 255)
            elif x in range(self.width_range[0], self.width_range[1]) and y in range(self.height_range[0], self.height_range[1]):
                self.bgImage.image = pyglet.resource.image("smallButtonHovered.png")
                self.lbl.element.color = (255, 255, 255, 255)
            else:
                self.bgImage.image = pyglet.resource.image("smallButton.png")
                self.lbl.element.color = (255, 255, 255, 255)

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self.showing:
            if x in range(self.width_range[0], self.width_range[1]) and y in range(self.height_range[0], self.height_range[1]):
                self.bgImage.image = pyglet.resource.image("smallButtonClicked.png")
                self.active = True
                self.lbl.element.color = (0, 0, 0, 255)
                if hasattr(self, "eventparam"):
                    self.eventName(self.eventparam)
                else:
                    self.eventName() 
                self.active = False
    
    def show(self, interval = 0.5):
        for child in self.get_children():
            child.do(FadeIn(interval))
        self.showing = True

    def hide(self, interval = 0.5):
        for child in self.get_children():
            child.do(FadeOut(interval))
        self.showing = False


class ChosenBox(layer.Layer):

    is_event_handler = True

    def __init__(self, gameMode):
        super().__init__()
        events.gamemenuevents.push_handlers(self)
        self.gameMode = gameMode
        self.bg = Sprite("chosenBox.png")
        self.width = self.bg.width
        self.height = self.bg.height
        self.gmTitle = Label("Chosen Game Mode:\n" + gameMode.name, color=(0, 0, 0, 255), font_size=15, anchor_x="left", anchor_y="center", multiline = True, width = self.width * 0.9, height = self.height * 0.9)
        self.gmTitle.x = self.x * 0.1
        self.gmTitle.y = self.y / 2
        self.delay = 0
        self.add(self.gmTitle, z=1)
        self.add(self.bg, z=0)
        self.active = False
        self.showing = True
        self.chosen = False
        self.width_range = [int((self.x) - (self.bg.width / 2)), int((self.x) + (self.bg.width / 2))]
        self.height_range = [int((self.y) - (self.bg.height / 2)), int((self.y) + (self.bg.width / 2))]

        self.schedule_interval(self.setWH, 1)
        self.resume_scheduler()

    def update_positions(self):
        self.gmTitle.x = -200
        self.gmTitle.y = -15

    def setWH(self, dt):
        x, y = director.window.width, director.window.height
        nmin = sc.scale(int((self.x) - (self.bg.width / 2)), int((self.y) - (self.bg.height / 2)))
        nmax = sc.scale(int((self.x) + (self.bg.width / 2)), int((self.y) + (self.bg.width / 2)))
        self.width_range = [int(nmin[0]), int(nmax[0])]
        self.height_range = [int(nmin[1]), int(nmax[1])]

    def on_mouse_motion(self, x, y, dx, dy):
        if not self.chosen and self.showing:
            if self.active:
                self.bg.image = pyglet.resource.image("chosenBoxClicked.png")
                self.gmTitle.element.color = (255, 255, 255, 255)
            elif x in range(self.width_range[0], self.width_range[1]) and y in range(self.height_range[0], self.height_range[1]):
                self.bg.image = pyglet.resource.image("chosenBoxHovered.png")
                self.gmTitle.element.color = (0, 0, 0, 255)
            else:
                self.bg.image = pyglet.resource.image("chosenBox.png")
                self.gmTitle.element.color = (0, 0, 0, 255)

    def on_mouse_press(self, x, y, buttons, modifiers):
        if not self.chosen and self.showing:
            if x in range(self.width_range[0], self.width_range[1]) and y in range(self.height_range[0], self.height_range[1]):
                self.bg.image = pyglet.resource.image("chosenBoxClicked.png")
                self.active = True
                self.gmTitle.element.color = (255, 255, 255, 255)
                events.gamemenuevents.onChosenBoxClick()
                self.active = False        

    def ExtendedInfoShow(self, gm):
        self.showing = False

    def ExtendedInfoHide(self, gm):
        self.do(Delay(0.7) + CallFunc(self.activate))

    def activate(self):
        self.showing = True

class LevelBox(layer.Layer):

    is_event_handler = True

    def __init__(self, level):
        super().__init__()
        events.gamemenuevents.push_handlers(self)
        self.level = level
        self.bg = Sprite("gameBox.png")
        self.thumbnail = Sprite(level.thumbnail)
        self.thumbnail.scale_x = 200 / self.thumbnail.width
        self.thumbnail.scale_y = 200 / self.thumbnail.height
        self.infoButton = smallButton("i", events.gamemenuevents.showExtendedInfo, eventparam=level.idx)
        self.width = self.bg.width
        self.height = self.bg.height
        self.thumbnail.x = self.x
        self.thumbnail.y = self.y * 0.6
        self.gmTitle = Label(level.name, color=(0, 0, 0, 255), font_size=20, anchor_x="left", anchor_y="center")
        self.gmTitle.x = self.x / 2
        self.gmTitle.y = self.y * 0.1
        self.delay = 0
        self.add(self.thumbnail, z=1)
        self.add(self.gmTitle, z=1)
        self.add(self.infoButton, z=1)
        self.add(self.bg, z=0)
        self.active = False
        self.showing = False
        self.chosen = False
        self.width_range = [int((self.x) - (self.bg.width / 2)), int((self.x) + (self.bg.width / 2))]
        self.height_range = [int((self.y) - (self.bg.height / 2)), int((self.y) + (self.bg.width / 2))]

        self.schedule_interval(self.setWH, 1)
        self.resume_scheduler()

    def show(self, duration = 0.5):
        if not self.showing:
            for child in self.get_children():
                if isinstance(child, smallButton):
                    child.do(Delay((self.delay / 4) + 1) + CallFunc(child.show))
                else:
                    child.do(FadeOut(0.00001) + Delay((self.delay / 4) + 1) + FadeIn(duration))
        self.showing = True

    def hide(self, duration = 0.5):
        if self.showing:
            for child in self.get_children():
                if isinstance(child, smallButton):
                    child.do(CallFunc(child.hide))
                else:
                    child.do(FadeOut(duration))
            self.showing = False

    def update_positions(self):
        self.thumbnail.x = 0
        self.thumbnail.y = 20
        self.gmTitle.x = -100
        self.gmTitle.y = -104
        self.infoButton.x = 80
        self.infoButton.y = -107
        self.infoButton.px = self.x
        self.infoButton.py = self.y

    def setWH(self, dt):
        x, y = director.window.width, director.window.height
        nmin = sc.scale(int((self.x) - (self.bg.width / 2)), int((self.y) - (self.bg.height / 2)))
        nmax = sc.scale(int((self.x) + (self.bg.width / 2)), int((self.y) + (self.bg.width / 2)))
        self.width_range = [int(nmin[0]), int(nmax[0])]
        self.height_range = [int(nmin[1]), int(nmax[1])]

    def on_mouse_motion(self, x, y, dx, dy):
        if not self.chosen and self.showing:
            if self.active:
                self.bg.image = pyglet.resource.image("gameBoxClicked.png")
                self.gmTitle.element.color = (255, 255, 255, 255)
            elif x in range(self.width_range[0], self.width_range[1]) and y in range(self.height_range[0], self.height_range[1]):
                if x in range(self.infoButton.width_range[0], self.infoButton.width_range[1]) and y in range(self.infoButton.height_range[0], self.infoButton.height_range[1]):
                    pass
                else:
                    self.bg.image = pyglet.resource.image("gameBoxHovered.png")
                    self.gmTitle.element.color = (0, 0, 0, 255)
            else:
                if x in range(self.infoButton.width_range[0], self.infoButton.width_range[1]) and y in range(self.infoButton.height_range[0], self.infoButton.height_range[1]):
                    pass
                else:
                    self.bg.image = pyglet.resource.image("gameBox.png")
                    self.gmTitle.element.color = (0, 0, 0, 255)

    def on_mouse_press(self, x, y, buttons, modifiers):
        if not self.chosen and self.showing:
            if x in range(self.width_range[0], self.width_range[1]) and y in range(self.height_range[0], self.height_range[1]):
                if x in range(self.infoButton.width_range[0], self.infoButton.width_range[1]) and y in range(self.infoButton.height_range[0], self.infoButton.height_range[1]):
                    pass
                else:
                    self.bg.image = pyglet.resource.image("gameBoxClicked.png")
                    self.active = True
                    self.gmTitle.element.color = (255, 255, 255, 255)
                    events.gamemenuevents.chooseLevel(self.level)
                    self.active = False        

    def ExtendedInfoShow(self, gm):
        self.showing = False

    def ExtendedInfoHide(self, gm):
        self.showing = True

class LVLExtendedInfo(layer.Layer):

    is_event_handler = True
    
    def __init__(self, level):
        super().__init__()
        events.gamemenuevents.push_handlers(self)
        self.level = level
        self.infoBox = Sprite("infoBox.png")
        self.bgDimmer = ColorLayer(0, 0, 0, 20)
        self.exitButton = smallButton("X", events.gamemenuevents.hideExtendedInfo, eventparam=self.level.idx)
        self.bgDimmer.opacity = 100
        self.infoBox.x = reswidth / 2
        self.infoBox.y = resheight / 2
        self.bgDimmer.width = reswidth
        self.bgDimmer.height = resheight
        self.exitButton.x = self.infoBox.x + ((self.infoBox.width / 2) * 0.91)
        self.exitButton.y = self.infoBox.y + ((self.infoBox.height / 2) * 0.85)
        self.active = False
        self.thumbnail = Sprite(level.thumbnail)
        self.thumbnail.scale_x = 350 / self.thumbnail.width
        self.thumbnail.scale_y = 350 / self.thumbnail.height
        self.thumbnail.x = self.infoBox.x - ((self.infoBox.width / 2) * 0.55)
        self.thumbnail.y = self.infoBox.y
        self.title = Label(level.name, anchor_x="center", anchor_y="center", font_size=39, color=(0, 0, 0, 255))
        self.title.x = self.infoBox.x + ((self.infoBox.width / 2) * 0.42)
        self.title.y = self.infoBox.y + ((self.infoBox.height / 2) * 0.7)
        self.desc = Label(level.desc, anchor_x="center", anchor_y="top", font_size=17, multiline = True, width=(self.infoBox.width * 0.5), height=(self.infoBox.height * 0.4), color=(0, 0, 0, 255), align="center")
        self.desc.x = self.infoBox.x + ((self.infoBox.width / 2) * 0.42)
        self.desc.y = self.infoBox.y + ((self.infoBox.height / 2) * 0.5)
        self.add(self.infoBox, z=5)
        self.add(self.bgDimmer, z=4)
        self.add(self.exitButton, z=5)
        self.add(self.thumbnail, z=5)
        self.add(self.title, z=5)
        self.add(self.desc, z=5)
        self.bgDimmer.do(FadeOut(0.00001))
        self.infoBox.do(FadeOut(0.00001))
        self.exitButton.do(FadeOut(0.00001))
        self.thumbnail.do(FadeOut(0.00001))
        self.title.do(FadeOut(0.00001))
        self.desc.do(FadeOut(0.00001))
        
       
    def ExtendedInfoShow(self, idx):
        if idx == self.level.idx and not self.active:
            self.infoBox.do(FadeIn(0.5))
            self.bgDimmer.do(FadeTo(150, 0.5))
            self.thumbnail.do(FadeIn(0.5))
            self.title.do(FadeIn(0.5))
            self.desc.do(FadeIn(0.5))
            self.exitButton.show()
            self.active = True
    
    def ExtendedInfoHide(self, idx):
        if idx == self.level.idx and self.active:
            self.infoBox.do(FadeOut(0.5))
            self.bgDimmer.do(FadeTo(0, 0.5))
            self.thumbnail.do(FadeOut(0.5))
            self.title.do(FadeOut(0.5))
            self.desc.do(FadeOut(0.5))
            self.exitButton.hide()
            self.active = False


class GameModeBox(layer.Layer):

    is_event_handler = True

    def __init__(self, gameMode):
        super().__init__()
        events.gamemenuevents.push_handlers(self)
        self.gameMode = gameMode
        self.bg = Sprite("gameBox.png")
        self.thumbnail = Sprite(gameMode.thumbnail)
        self.thumbnail.scale_x = 200 / self.thumbnail.width
        self.thumbnail.scale_y = 200 / self.thumbnail.height
        self.infoButton = smallButton("i", events.gamemenuevents.showExtendedInfo, eventparam=gameMode.idx)
        self.width = self.bg.width
        self.height = self.bg.height
        self.thumbnail.x = self.x
        self.thumbnail.y = self.y * 0.6
        self.gmTitle = Label(gameMode.name, color=(0, 0, 0, 255), font_size=20, anchor_x="left", anchor_y="center")
        self.gmTitle.x = self.x / 2
        self.gmTitle.y = self.y * 0.1
        self.delay = 0
        self.add(self.thumbnail, z=1)
        self.add(self.gmTitle, z=1)
        self.add(self.infoButton, z=1)
        self.add(self.bg, z=0)
        self.active = False
        self.showing = False
        self.chosen = False
        self.width_range = [int((self.x) - (self.bg.width / 2)), int((self.x) + (self.bg.width / 2))]
        self.height_range = [int((self.y) - (self.bg.height / 2)), int((self.y) + (self.bg.width / 2))]

        self.schedule_interval(self.setWH, 1)
        self.resume_scheduler()

    def show(self, duration = 0.5, cdelay = 0):
        if not self.showing:
            for child in self.get_children():
                if isinstance(child, smallButton):
                    child.do(Delay(cdelay + (self.delay / 4)) + CallFunc(child.show))
                else:
                    child.do(FadeOut(0.00001) + Delay(cdelay + (self.delay / 4)) + FadeIn(duration))
        self.showing = True

    def hide(self, duration = 0.5):
        if self.showing:
            for child in self.get_children():
                if isinstance(child, smallButton):
                    child.do(CallFunc(child.hide))
                else:
                    child.do(FadeOut(duration))
            self.showing = False

    def update_positions(self):
        self.thumbnail.x = 0
        self.thumbnail.y = 20
        self.gmTitle.x = -100
        self.gmTitle.y = -104
        self.infoButton.x = 80
        self.infoButton.y = -107
        self.infoButton.px = self.x
        self.infoButton.py = self.y

    def setWH(self, dt):
        x, y = director.window.width, director.window.height
        nmin = sc.scale(int((self.x) - (self.bg.width / 2)), int((self.y) - (self.bg.height / 2)))
        nmax = sc.scale(int((self.x) + (self.bg.width / 2)), int((self.y) + (self.bg.width / 2)))
        self.width_range = [int(nmin[0]), int(nmax[0])]
        self.height_range = [int(nmin[1]), int(nmax[1])]

    def on_mouse_motion(self, x, y, dx, dy):
        if not self.chosen and self.showing:
            if self.active:
                self.bg.image = pyglet.resource.image("gameBoxClicked.png")
                self.gmTitle.element.color = (255, 255, 255, 255)
            elif x in range(self.width_range[0], self.width_range[1]) and y in range(self.height_range[0], self.height_range[1]):
                if x in range(self.infoButton.width_range[0], self.infoButton.width_range[1]) and y in range(self.infoButton.height_range[0], self.infoButton.height_range[1]):
                    pass
                else:
                    self.bg.image = pyglet.resource.image("gameBoxHovered.png")
                    self.gmTitle.element.color = (0, 0, 0, 255)
            else:
                if x in range(self.infoButton.width_range[0], self.infoButton.width_range[1]) and y in range(self.infoButton.height_range[0], self.infoButton.height_range[1]):
                    pass
                else:
                    self.bg.image = pyglet.resource.image("gameBox.png")
                    self.gmTitle.element.color = (0, 0, 0, 255)

    def on_mouse_press(self, x, y, buttons, modifiers):
        if not self.chosen and self.showing:
            if x in range(self.width_range[0], self.width_range[1]) and y in range(self.height_range[0], self.height_range[1]):
                if x in range(self.infoButton.width_range[0], self.infoButton.width_range[1]) and y in range(self.infoButton.height_range[0], self.infoButton.height_range[1]):
                    pass
                else:
                    self.bg.image = pyglet.resource.image("gameBoxClicked.png")
                    self.active = True
                    self.gmTitle.element.color = (255, 255, 255, 255)
                    events.gamemenuevents.chooseGameMode(self.gameMode)
                    self.active = False        

    def ExtendedInfoShow(self, gm):
        self.showing = False

    def ExtendedInfoHide(self, gm):
        self.showing = True

class GMExtendedInfo(layer.Layer):

    is_event_handler = True
    
    def __init__(self, gameMode):
        super().__init__()
        events.gamemenuevents.push_handlers(self)
        self.gameMode = gameMode
        self.infoBox = Sprite("infoBox.png")
        self.bgDimmer = ColorLayer(0, 0, 0, 20)
        self.exitButton = smallButton("X", events.gamemenuevents.hideExtendedInfo, eventparam=self.gameMode.idx)
        self.bgDimmer.opacity = 100
        self.infoBox.x = reswidth / 2
        self.infoBox.y = resheight / 2
        self.bgDimmer.width = reswidth
        self.bgDimmer.height = resheight
        self.exitButton.x = self.infoBox.x + ((self.infoBox.width / 2) * 0.91)
        self.exitButton.y = self.infoBox.y + ((self.infoBox.height / 2) * 0.85)
        self.active = False
        self.thumbnail = Sprite(gameMode.thumbnail)
        self.thumbnail.scale_x = 350 / self.thumbnail.width
        self.thumbnail.scale_y = 350 / self.thumbnail.height
        self.thumbnail.x = self.infoBox.x - ((self.infoBox.width / 2) * 0.55)
        self.thumbnail.y = self.infoBox.y
        self.title = Label(gameMode.name, anchor_x="center", anchor_y="center", font_size=39, color=(0, 0, 0, 255))
        self.title.x = self.infoBox.x + ((self.infoBox.width / 2) * 0.42)
        self.title.y = self.infoBox.y + ((self.infoBox.height / 2) * 0.7)
        self.desc = Label(gameMode.desc, anchor_x="center", anchor_y="top", font_size=17, multiline = True, width=(self.infoBox.width * 0.5), height=(self.infoBox.height * 0.4), color=(0, 0, 0, 255), align="center")
        self.desc.x = self.infoBox.x + ((self.infoBox.width / 2) * 0.42)
        self.desc.y = self.infoBox.y + ((self.infoBox.height / 2) * 0.5)
        self.add(self.infoBox, z=5)
        self.add(self.bgDimmer, z=4)
        self.add(self.exitButton, z=5)
        self.add(self.thumbnail, z=5)
        self.add(self.title, z=5)
        self.add(self.desc, z=5)
        self.bgDimmer.do(FadeOut(0.00001))
        self.infoBox.do(FadeOut(0.00001))
        self.exitButton.hide(0.00001)
        self.thumbnail.do(FadeOut(0.00001))
        self.title.do(FadeOut(0.00001))
        self.desc.do(FadeOut(0.00001))
        
       
    def ExtendedInfoShow(self, idx):
        if idx == self.gameMode.idx and not self.active:
            self.infoBox.do(FadeIn(0.5))
            self.bgDimmer.do(FadeTo(150, 0.5))
            self.thumbnail.do(FadeIn(0.5))
            self.title.do(FadeIn(0.5))
            self.desc.do(FadeIn(0.5))
            self.exitButton.show()
            self.active = True
    
    def ExtendedInfoHide(self, idx):
        if idx == self.gameMode.idx and self.active:
            self.infoBox.do(FadeOut(0.5))
            self.bgDimmer.do(FadeTo(0, 0.5))
            self.thumbnail.do(FadeOut(0.5))
            self.title.do(FadeOut(0.5))
            self.desc.do(FadeOut(0.5))
            self.exitButton.hide()
            self.active = False