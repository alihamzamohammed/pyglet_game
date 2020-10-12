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

        self.clickable = True

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
        if self.clickable:
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
        if self.clickable:
            if x in range(self.width_range[0], self.width_range[1]) and y in range(self.height_range[0], self.height_range[1]):
                self.bgImage.image = pyglet.resource.image("settingsCategoryButtonClicked.png")
                self.active = True
                self.lbl.element.color = (0, 0, 0, 255)
                self.eventName()


"""Large Button. Same as toggle button, but for activating events"""
class LargeButton(layer.Layer):

    is_event_handler = True

    def __init__(self, label, eventName, selfx, selfy, parent = None, active = False, *args, **kwargs):
        super().__init__()
        global x, y

        self.eventName = eventName
        self.active = active
        if "eventparam" in kwargs:
            self.eventparam = kwargs["eventparam"]

        self.bgImage = Sprite("largeButton.png")
        self.lbl = Label(label, anchor_x="center", anchor_y="center", dpi=110, font_size=16)
        self.width = self.bgImage.width
        self.height = self.bgImage.height
        #self.x = 0
        #self.y = 0
        if not parent == None:
            self.px = parent.x
            self.py = parent.y
        else:
            self.px = 0
            self.py = 0
        pwidth = parent.width
        pheight = parent.height
        self.x = pwidth * selfx
        self.y = pheight * selfy

        self.width_range = [int((self.px + self.x) - (self.bgImage.width / 2)), int((self.px + self.x) + (self.bgImage.width / 2))]
        self.height_range = [int((self.py + self.y) - (self.bgImage.height / 2)), int((self.py + self.y) + (self.bgImage.height / 2))]

        self.add(self.bgImage)
        self.add(self.lbl)

        self.showing = True

        self.schedule_interval(self.setWH, 1)
        self.resume_scheduler()

    def setWH(self, dt):
        x, y = director.window.width, director.window.height
        #nmin = sc.scale(int((self.px + self.x) - (self.bgImage.width / 2)), int((self.py + self.y) - (self.bgImage.height / 2)))
        #nmax = sc.scale(int((self.px + self.x) + (self.bgImage.width / 2)), int((self.py + self.y) + (self.bgImage.height / 2)))
        nmin = sc.scale(int(self.px + (self.x - (self.width / 2))), int(self.py + (self.y - (self.height / 2))))
        nmax = sc.scale(int(self.px + (self.x + (self.width / 2))), int(self.py + (self.y + (self.height / 2))))
        self.width_range = [int(nmin[0]), int(nmax[0])]
        self.height_range = [int(nmin[1]), int(nmax[1])]

    def on_mouse_motion(self, x, y, dx, dy):
        print(x, y)
        if self.showing:
            print("showing")
            if self.active:
                self.bgImage.image = pyglet.resource.image("largeButtonClicked.png")
                self.lbl.element.color = (0, 0, 0, 255)
            elif x in range(self.width_range[0], self.width_range[1]) and y in range(self.height_range[0], self.height_range[1]):
                print("active")
                self.bgImage.image = pyglet.resource.image("largeButtonHovered.png")
                self.lbl.element.color = (255, 255, 255, 255)
            else:
                self.bgImage.image = pyglet.resource.image("largeButton.png")
                self.lbl.element.color = (255, 255, 255, 255)

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self.showing:
            if x in range(self.width_range[0], self.width_range[1]) and y in range(self.height_range[0], self.height_range[1]):
                self.bgImage.image = pyglet.resource.image("largeButtonClicked.png")
                self.active = True
                self.lbl.element.color = (0, 0, 0, 255)
                if hasattr(self, "eventparam"):
                    self.eventName(self.eventparam)
                else:
                    self.eventName() 
                self.active = False


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
        self.bgImage = Sprite("largeButton.png")
        self.active = True if self.configDict[self.section][self.option] == "True" else False
        self.changed = False
        if self.active:
            self.bgImage.image = pyglet.resource.image("largeToggledButton.png")
            self.lbl.element.text = "YES"
        else:
            self.bgImage.image = pyglet.resource.image("largeButton.png")
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
                self.bgImage.image = pyglet.resource.image("largeToggledButtonHovered.png")
            else:
                self.bgImage.image = pyglet.resource.image("largeButtonHovered.png")
        else:
            if self.active:
                self.bgImage.image = pyglet.resource.image("largeToggledButton.png")
            else:
                self.bgImage.image = pyglet.resource.image("largeButton.png")

    def on_mouse_press(self, x, y, buttons, modifiers):
        if x in range(self.width_range[0], self.width_range[1]) and y in range(self.height_range[0], self.height_range[1]):
            self.active = not self.active
            self.changed = True
            self.configDict[self.section][self.option] = str(self.active)
            if callable(self.command):
                self.command(self.active)
            if self.active:
                self.bgImage.image = pyglet.resource.image("largeToggledButtonClicked.png")
                self.lbl.element.text = "YES"
            else:
                self.bgImage.image = pyglet.resource.image("largeButtonClicked.png")
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
        self.height_range = [int((self.py + self.y) - (self.bgImage.height / 2)), int((self.py + self.y) + (self.bgImage.height / 2))]

        self.add(self.bgImage)
        self.add(self.lbl)

        self.hide(0.01)
        self.showing = False

        self.schedule_interval(self.setWH, 1)
        self.resume_scheduler()

    def setWH(self, dt):
        x, y = director.window.width, director.window.height
        nmin = sc.scale(int((self.px + self.x) - (self.bgImage.width / 2)), int((self.py + self.y) - (self.bgImage.height / 2)))
        nmax = sc.scale(int((self.px + self.x) + (self.bgImage.width / 2)), int((self.py + self.y) + (self.bgImage.height / 2)))
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
        self.height_range = [int((self.py + self.y) - (self.bgImage.height / 2)), int((self.py + self.y) + (self.bgImage.height / 2))]

        self.add(self.bgImage)
        self.add(self.lbl)

        self.hide(0.01)
        self.showing = False

        self.schedule_interval(self.setWH, 1)
        self.resume_scheduler()

    def setWH(self, dt):
        x, y = director.window.width, director.window.height
        nmin = sc.scale(int((self.px + self.x) - (self.bgImage.width / 2)), int((self.py + self.y) - (self.bgImage.height / 2)))
        nmax = sc.scale(int((self.px + self.x) + (self.bgImage.width / 2)), int((self.py + self.y) + (self.bgImage.height / 2)))
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


class SettingsAboutBox(layer.Layer):

    is_event_handler = True
    
    def __init__(self):
        super().__init__()
        events.settingsevents.push_handlers(self)
        self.infoBox = Sprite("infoBox.png")
        self.bgDimmer = layer.ColorLayer(0, 0, 0, 20)
        self.exitButton = smallButton("X", events.settingsevents.aboutPopupHide)
        self.bgDimmer.opacity = 100
        self.infoBox.x = reswidth / 2
        self.infoBox.y = resheight / 2
        self.bgDimmer.width = reswidth
        self.bgDimmer.height = resheight
        self.exitButton.x = self.infoBox.x + ((self.infoBox.width / 2) * 0.91)
        self.exitButton.y = self.infoBox.y + ((self.infoBox.height / 2) * 0.85)
        self.active = False
        self.title = Label("title", anchor_x="center", anchor_y="center", font_size=39, color=(0, 0, 0, 255))
        self.title.x = self.infoBox.x
        self.title.y = self.infoBox.y + ((self.infoBox.height / 2) * 0.8)
        self.desc = Label("desc", anchor_x="center", anchor_y="top", font_size=17, multiline = True, width=(self.infoBox.width * 0.87), height=(self.infoBox.height * 0.4), color=(0, 0, 0, 255), align="center")
        self.desc.x = self.infoBox.x
        self.desc.y = self.infoBox.y + ((self.infoBox.height / 2) * 0.6)
        self.add(self.infoBox, z=5)
        self.add(self.bgDimmer, z=4)
        self.add(self.exitButton, z=5)
        self.add(self.title, z=5)
        self.add(self.desc, z=5)
        self.bgDimmer.do(FadeOut(0.00001))
        self.infoBox.do(FadeOut(0.00001))
        self.exitButton.do(FadeOut(0.00001))
        self.title.do(FadeOut(0.00001))
        self.desc.do(FadeOut(0.00001))
        
       
    def showAboutPopup(self):
        if not self.active:
            self.infoBox.do(FadeIn(0.75))
            self.bgDimmer.do(FadeTo(150, 0.75))
            self.title.do(FadeIn(0.75))
            self.desc.do(FadeIn(0.75))
            self.exitButton.show()
            self.active = True
    
    def hideAboutPopup(self):
        if self.active:
            self.infoBox.do(FadeOut(0.75))
            self.bgDimmer.do(FadeTo(0, 0.75))
            self.title.do(FadeOut(0.75))
            self.desc.do(FadeOut(0.75))
            self.exitButton.hide()
            self.active = False

