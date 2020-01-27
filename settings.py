import cocos
import os
import logger
from cocos.text import Label
from cocos import scene
from cocos import layer
from cocos.actions import *
from cocos.menu import *
from cocos.sprite import *
from cocos.director import director
import cfg
import events
import pyglet
import pyglet.gl
import threading
from pyglet import event
import resources
import random
import time

x, y = director.window.width, director.window.height
reswidth, resheight = [int(res) for res in cfg.configuration["Core"]["defaultres"].split("x")]

class sectionButton(layer.Layer): 

    is_event_handler = True

    def __init__(self, label, eventName, buttonorder = 1, active = False):
        super().__init__()
        global x, y

        self.eventName = eventName
        self.active = active

        self.bgImage = Sprite("settingsCategoryButton.png")
        self.lbl = Label(label, anchor_x="center", anchor_y="center")
        
        self.x = x * (0.2 * buttonorder)
        self.y = y * 0.76
        
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


class MessagePopup(layer.ColorLayer):

    def __init__(self):
        super().__init__(50, 50, 50, 255)
        global x, y
        self.width = int(x)
        self.height = int(y * 0.1)
        self.x = 0
        self.y = int(-self.height)
        self.lbl = Label("message", font_size = 18, anchor_y = "center")
        self.lbl.x = int(self.width * 0.05)
        self.lbl.y = int(self.height / 2)
        self.add(self.lbl)
        self.active = False
    
    def showMessage(self, message):
        if not self.active:
            self.lbl.element.text = message
            self.do(AccelDeccel(MoveTo((int(self.x), 0), duration = 0.5)))
            self.active = True

messagePopup = MessagePopup()

class ToggleButton(layer.Layer):

    is_event_handler = True

    def __init__(self, parent, selfx, selfy, configDict, section, option, command = None, restartGame = False):
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
        self.restartGame = restartGame
        self.lbl = Label("YES", anchor_x="center", anchor_y="center")
        self.bgImage = Sprite("toggleButton.png")
        self.active = True if self.configDict[self.section][self.option] == "True" else False
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
        scalex = x / reswidth
        scaley = y / resheight
        self.width_range = [int((self.px * scalex) + ((self.x * scalex) - (self.width * scalex) / 2)), int((self.px * scalex) + ((self.x * scalex) + (self.width * scalex) / 2))]
        self.height_range = [int((self.py * scaley) + ((self.y * scaley) - (self.height * scaley) / 2)), int((self.py * scaley) + ((self.y * scaley) + (self.height * scaley) / 2))]
    
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
            if self.restartGame:
                messagePopup.showMessage("Your game must be restarted in order to apply these settings.")
            self.active = not self.active
            self.configDict[self.section][self.option] = str(self.active)
            if callable(self.command):
                self.command(self.active)
            if self.active:
                self.bgImage.image = pyglet.resource.image("toggledButtonClicked.png")
                self.lbl.element.text = "YES"
            else:
                self.bgImage.image = pyglet.resource.image("toggleButtonClicked.png")
                self.lbl.element.text = "NO"


class VideoSettings(layer.ColorLayer):

    is_event_handler = True

    def __init__(self):        
        super().__init__(100, 100, 100, 100)
        events.settingsevents.push_handlers(self)
        global x, y
        self.width = int(x * 0.75)
        self.height = int(y * 0.6)
        self.x = int((x / 2) - (self.width / 2))
        self.y = int((y * 0.37) - (self.height / 2))
        self.active = True
        self.posleft = int(-self.width)
        self.poscenter = int((x / 2) - (self.width / 2))
        self.posright = int(x)

        fullscreenLabel = Label("Fullscreen", font_size=25, anchor_x="left", anchor_y="center", color=(255, 255, 255, 255))
        fullscreenLabel.x = self.width * 0.05
        fullscreenLabel.y = self.height * 0.9
        fullscreenButton = ToggleButton(self, 0.9, 0.9, cfg.configuration, section = "Core", option = "fullscreen", command = director.window.set_fullscreen)

        vsyncLabel = Label("VSync", font_size=25, anchor_x="left", anchor_y="center", color=(255, 255, 255, 255))
        vsyncLabel.x = self.width * 0.05
        vsyncLabel.y = self.height * 0.7
        vsyncButton = ToggleButton(self, 0.9, 0.7, cfg.configuration, section = "Core", option = "vsync", command = director.window.set_vsync)

        showfpsLabel = Label("Show FPS", font_size=25, anchor_x="left", anchor_y="center", color=(255, 255, 255, 255))
        showfpsLabel.x = self.width * 0.05
        showfpsLabel.y = self.height * 0.5
        showfpsButton = ToggleButton(self, 0.9, 0.5, cfg.configuration, section = "Core", option = "showfps", command = director.set_show_FPS)

        self.add(fullscreenButton)
        self.add(fullscreenLabel)
        self.add(vsyncButton)
        self.add(vsyncLabel)
        self.add(showfpsButton)
        self.add(showfpsLabel)

    def showVideoScreen(self):
        self.active = True
        self.do(AccelDeccel(MoveTo((self.poscenter, self.y), duration = 0.5)))

    def showSoundScreen(self):
        if self.active:
            self.do(AccelDeccel(MoveTo((self.posleft, self.y), duration = 0.5)))
            self.active = False
        else:
            self.x = self.posleft

    def showExtensionsScreen(self):
        if self.active:
            self.do(AccelDeccel(MoveTo((self.posleft, self.y), duration = 0.5)))
            self.active = False
        else:
            self.x = self.posleft

    def showAboutScreen(self):
        if self.active:
            self.do(AccelDeccel(MoveTo((self.posleft, self.y), duration = 0.5)))
            self.active = False
        else:
            self.x = self.posleft    


class SoundSettings(layer.ColorLayer):

    is_event_handler = True

    def __init__(self):
        super().__init__(0, 0, 255, 255)
        events.settingsevents.push_handlers(self)
        global x, y
        self.width = int(x * 0.75)
        self.height = int(y * 0.6)
        self.posleft = int(-self.width)
        self.poscenter = int((x / 2) - (self.width / 2))
        self.posright = int(x)
        self.x = self.posright
        self.y = int((y * 0.37) - (self.height / 2))
        self.active = False

    def showVideoScreen(self):
        if self.active:
            self.do(AccelDeccel(MoveTo((self.posright, self.y), duration = 0.5)))
            self.active = False
        else:
            self.x = self.posright

    def showSoundScreen(self):
        self.active = True
        self.do(AccelDeccel(MoveTo((self.poscenter, self.y), duration = 0.5)))

    def showExtensionsScreen(self):
        if self.active:
            self.do(AccelDeccel(MoveTo((self.posleft, self.y), duration=0.5)))
            self.active = False
        else:
            self.x = self.posleft

    def showAboutScreen(self):
        if self.active:
            self.do(AccelDeccel(MoveTo((self.posleft, self.y), duration=0.5)))
            self.active = False
        else:
            self.x = self.posleft


class ExtensionSettings(layer.ColorLayer):

    is_event_handler = True

    def __init__(self):
        super().__init__(0, 255, 0, 255)
        events.settingsevents.push_handlers(self)
        global x, y
        self.width = int(x * 0.75)
        self.height = int(y * 0.6)
        self.posleft = int(-self.width)
        self.poscenter = int((x / 2) - (self.width / 2))
        self.posright = int(x)
        self.x = self.posright
        self.y = int((y * 0.37) - (self.height / 2))
        self.active = False
        
    def showVideoScreen(self):
        if self.active:
            self.do(AccelDeccel(MoveTo((self.posright, self.y), duration = 0.5)))
            self.active = False
        else:
            self.x = self.posright

    def showSoundScreen(self):
        if self.active:
            self.do(AccelDeccel(MoveTo((self.posright, self.y), duration = 0.5)))
            self.active = False
        else:
            self.x = self.posright

    def showExtensionsScreen(self):
        self.active = True
        self.do(AccelDeccel(MoveTo((self.poscenter, self.y), duration = 0.5)))

    def showAboutScreen(self):
        if self.active:
            self.do(AccelDeccel(MoveTo((self.posleft, self.y), duration = 0.5)))
            self.active = False
        else:
            self.x = self.posleft


class AboutSettings(layer.ColorLayer):

    is_event_handler = True

    def __init__(self):
        super().__init__(255, 0, 0, 255)
        events.settingsevents.push_handlers(self)
        global x, y
        self.width = int(x * 0.75)
        self.height = int(y * 0.6)
        self.posleft = int(-self.width)
        self.poscenter = int((x / 2) - (self.width / 2))
        self.posright = int(x)
        self.x = self.posright
        self.y = int((y * 0.37) - (self.height / 2))
        self.active = False

    def showVideoScreen(self):
        if self.active:
            self.do(AccelDeccel(MoveTo((self.posright, self.y), duration = 0.5)))
            self.active = False
        else:
            self.x = self.posright

    def showSoundScreen(self):
        if self.active:
            self.do(AccelDeccel(MoveTo((self.posright, self.y), duration = 0.5)))
            self.active = False
        else:
            self.x = self.posright

    def showExtensionsScreen(self):
        if self.active:
            self.do(AccelDeccel(MoveTo((self.posright, self.y), duration = 0.5)))
            self.active = False
        else:
            self.x = self.posright

    def showAboutScreen(self):
        self.active = True
        self.do(AccelDeccel(MoveTo((self.poscenter, self.y), duration = 0.5)))


class SettingsScreen(scene.Scene):

    def __init__(self):
        super().__init__() 
        global x, y
        settingsLabel = cocos.text.Label(
            "Settings",
            font_name=resources.font[1],
            font_size=50,
            anchor_y="center",
            anchor_x="center"
        )
        settingsLabel.position = x / 2, y * 0.9
        
        videoButton = sectionButton("Video", events.settingsevents.onVideoButtonClick, 1)
        soundButton = sectionButton("Sound", events.settingsevents.onSoundButtonClick, 2)
        expansionButton = sectionButton("Expansion", events.settingsevents.onExtensionsButtonClick, 3)
        aboutButton = sectionButton("About", events.settingsevents.onAboutButtonClick, 4)
        backButton = sectionButton("Back", events.mainmenuevents.backToMainMenu)
        backButton.x = x * 0.15
        backButton.y = y * 0.89

        self.add(videoButton)
        self.add(soundButton)
        self.add(expansionButton)
        self.add(aboutButton)
        self.add(backButton)
        self.add(settingsLabel)
        videoSettings = VideoSettings()
        soundSettings = SoundSettings()
        extensionSettings = ExtensionSettings()
        aboutSettings = AboutSettings()
        self.add(videoSettings)
        self.add(soundSettings)
        self.add(extensionSettings)
        self.add(aboutSettings)

        self.add(messagePopup)

    def on_enter(self):
        super().on_enter()
