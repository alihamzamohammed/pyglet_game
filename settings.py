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
import elements
import resources
import random
import time
import modes, levels, items

x, y = director.window.width, director.window.height
reswidth, resheight = [int(res) for res in cfg.resolution.split("x")]


class SettingsSectionButton(elements.sectionButton):

    def __init__(self, label, eventName, active = False, buttonorder = 1):
        super().__init__(label, eventName, active)
        global x, y
        self.x = x * (0.2 * buttonorder)
        self.y = y * 0.76
        events.settingsevents.push_handlers(self)

    def showAboutPopup(self):
        self.clickable = False

    def hideAboutPopup(self):
        self.do(Delay(1) + CallFunc(self.hideAboutBox2))

    def hideAboutBox2(self):
        self.clickable = True


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

class SettingsToggleButton(elements.ToggleButton):

    is_event_handler = True

    def __init__(self, parent, selfx, selfy, configDict, section, option, command = None, restartGame = False):
        super().__init__(parent, selfx, selfy, configDict, section, option, command)
        self.restartGame = restartGame
        self.schedule(self.checkChanged)
        self.resume_scheduler()

    def checkChanged(self, dt):
        if self.changed and self.restartGame:
            messagePopup.showMessage("Your game must be restarted in order to apply these settings.")

class VideoSettings(layer.ColorLayer):

    is_event_handler = True

    class ResolutionInput(layer.Layer):

        def __init__(self, parent):
            super().__init__()
            reswidth, resheight = [int(res) for res in cfg.configuration["Core"]["defaultres"].split("x")]
            self.txtBoxWidth = elements.TextBox(self, 0, 0, default_text=str(reswidth), charLimit=4)
            seperator = Label("X", anchor_x = "center", anchor_y = "center", font_size = 15, color = (255, 255, 255, 255))
            seperator.x = self.txtBoxWidth.width
            seperator.y = 0
            self.width = (self.txtBoxWidth.width * 2)
            self.height = self.txtBoxWidth.height
            self.txtBxHeight = elements.TextBox(self, self.width, 0, default_text=str(resheight), charLimit=4)
            self.x = parent.width - (self.width + (parent.width * 0.1))
            self.y = parent.height * 0.3
            self.txtBoxWidth.parentx = parent.x + self.x
            self.txtBoxWidth.parenty = parent.y + self.y
            self.txtBxHeight.parentx = parent.x + self.x
            self.txtBxHeight.parenty = parent.y + self.y
            self.add(self.txtBoxWidth)
            self.add(seperator)
            self.add(self.txtBxHeight)
            self.schedule_interval(self.changed, 0.5)
            self.resume_scheduler()

        def changed(self, dt):
            if self.txtBoxWidth.changed or self.txtBxHeight.changed:
                messagePopup.showMessage("Your game needs to be restarted for these changes to take effect.")
                cfg.configuration["Core"]["defaultres"] = str(self.txtBoxWidth.get_text()) + "x" + str(self.txtBxHeight.get_text())

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
        fullscreenButton = SettingsToggleButton(self, 0.9, 0.9, cfg.configuration, section = "Core", option = "fullscreen", command = director.window.set_fullscreen)

        vsyncLabel = Label("VSync", font_size=25, anchor_x="left", anchor_y="center", color=(255, 255, 255, 255))
        vsyncLabel.x = self.width * 0.05
        vsyncLabel.y = self.height * 0.7
        vsyncButton = SettingsToggleButton(self, 0.9, 0.7, cfg.configuration, section = "Core", option = "vsync", command = director.window.set_vsync)

        showfpsLabel = Label("Show FPS", font_size=25, anchor_x="left", anchor_y="center", color=(255, 255, 255, 255))
        showfpsLabel.x = self.width * 0.05
        showfpsLabel.y = self.height * 0.5
        showfpsButton = SettingsToggleButton(self, 0.9, 0.5, cfg.configuration, section = "Core", option = "showfps", command = director.set_show_FPS)

        resInputLabel = Label("Resolution", font_size=25, anchor_x="left", anchor_y="center", color=(255, 255, 255, 255))
        resInputLabel.x = self.width * 0.05
        resInputLabel.y = self.height * 0.3
        resInput = self.ResolutionInput(self)

        self.add(fullscreenButton)
        self.add(fullscreenLabel)
        self.add(vsyncButton)
        self.add(vsyncLabel)
        self.add(showfpsButton)
        self.add(showfpsLabel)
        self.add(resInput)
        self.add(resInputLabel)

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

    def showMiscScreen(self):
        if self.active:
            self.do(AccelDeccel(MoveTo((self.posleft, self.y), duration = 0.5)))
            self.active = False
        else:
            self.x = self.posleft

#TODO: Sound settings
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

    def showMiscScreen(self):
        if self.active:
            self.do(AccelDeccel(MoveTo((self.posleft, self.y), duration=0.5)))
            self.active = False
        else:
            self.x = self.posleft

#TODO: Extension settings
#?: Maybe change this to controls instead of extensions
class ExtensionSettings(layer.ColorLayer):

    is_event_handler = True

    class ExtensionList(layer.Layer):

        def __init__(self):
            super().__init__()
            
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

    def showMiscScreen(self):
        if self.active:
            self.do(AccelDeccel(MoveTo((self.posleft, self.y), duration = 0.5)))
            self.active = False
        else:
            self.x = self.posleft

#TODO: Misc settings
class MiscSettings(layer.ColorLayer):

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

        #miscInfo = Label("Coming Soon", anchor_x="center", anchor_y="center", font_size=35, multiline=True, width=(self.width * 0.8), align="center")
        #miscInfo.x = self.width / 2
        #miscInfo.y = self.height / 2
        #self.add(miscInfo)
        controlsButton = elements.LargeButton("Controls", eventname = events.settingsevents.onControlsButtonClick)
        controlsButton.x = self.width / 2
        controlsButton.y = self.height / 2
        self.add(controlsButton)


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

    def showMiscScreen(self):
        self.active = True
        self.do(AccelDeccel(MoveTo((self.poscenter, self.y), duration = 0.5)))


class SettingsScreen(scene.Scene):

    is_event_handler = True

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
        events.settingsevents.push_handlers(self)

        self.videoButton = SettingsSectionButton("Video", events.settingsevents.onVideoButtonClick, buttonorder = 1, active = True)
        self.soundButton = SettingsSectionButton("Sound", events.settingsevents.onSoundButtonClick, buttonorder = 2)
        self.extensionButton = SettingsSectionButton("Expansion", events.settingsevents.onExtensionsButtonClick, buttonorder = 3)
        self.miscButton = SettingsSectionButton("Miscallaneous", events.settingsevents.onMiscButtonClick, buttonorder = 4)
        backButton = elements.mediumButton("Back", events.mainmenuevents.backToMainMenu)
        aboutButton = elements.mediumButton("About", events.settingsevents.aboutPopupShow)
        aboutPopup = elements.SettingsAboutBox()

        backButton.x = x * 0.15
        backButton.y = y * 0.89
        backButton.show(0.01)
        aboutButton.x = x * 0.85
        aboutButton.y = y * 0.89
        aboutButton.show(0.01)

        aboutPopup.title.element.text = "About Game"
        aboutPopup.desc.element.text = "Written and programmed by Ali Hamza Mohammed.\n\nWORK IN PROGRESS\nStill to add:\nSound system\nLevel editor\nMultiplayer functionality\nGeneral visual tweaks\nDefault resource packs\n\nSource code for this game is available at github.com/alihamzamohammed/coursework\n\n\nInstalled Game Modes: " + str(len(modes.gamemodes)) + "    Installed Levels: " + str(len(levels.levels)) + "    Installed Item Packs: " + str(len(items.itempacks))
        
        self.add(self.videoButton)
        self.add(self.soundButton)
        self.add(self.extensionButton)
        self.add(self.miscButton)
        self.add(backButton)
        self.add(aboutButton)
        self.add(settingsLabel)
        self.add(aboutPopup, z=2)

        videoSettings = VideoSettings()
        soundSettings = SoundSettings()
        extensionSettings = ExtensionSettings()
        miscSettings = MiscSettings()

        self.add(videoSettings)
        self.add(soundSettings)
        self.add(extensionSettings)
        self.add(miscSettings)

        self.add(messagePopup)

    def on_enter(self):
        super().on_enter()

    def showVideoScreen(self):
        self.videoButton.active = True
        self.soundButton.active = False
        self.extensionButton.active = False
        self.miscButton.active = False
        
    def showSoundScreen(self):
        self.videoButton.active = False
        self.soundButton.active = True
        self.extensionButton.active = False
        self.miscButton.active = False    

    def showExtensionsScreen(self):
        self.videoButton.active = False
        self.soundButton.active = False
        self.extensionButton.active = True
        self.miscButton.active = False

    def showmiscScreen(self):
        self.videoButton.active = False
        self.soundButton.active = False
        self.extensionButton.active = False
        self.miscButton.active = True