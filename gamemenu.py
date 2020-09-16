import cocos
import pyglet
import os
import logger
import resources
import cfg
from cocos.director import director
from cocos.scene import Scene
from cocos.layer import *
from cocos.actions import *
from cocos.sprite import *
from cocos.text import *
import levels
import modes
import events
import elements # TODO: All elements in this class will be moved over, maybe?

import scaling as sc

x, y = director.window.width, director.window.height
reswidth, resheight = [int(res) for res in cfg.resolution.split("x")]

title = cocos.text.Label(
    "Game Modes",
    font_name=resources.font[1],
    font_size=50,
    anchor_y="top",
    anchor_x="left"
)

"""Small button. Same as small button, but can contain more text"""
class mediumButton(Layer):

    is_event_handler = True

    def __init__(self, label, eventName, active = False, *args, **kwargs):
        super().__init__()
        global x, y

        self.eventName = eventName
        self.active = active
        print(args, kwargs)
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
class smallButton(Layer):

    is_event_handler = True

    def __init__(self, label, eventName, active = False, *args, **kwargs):
        super().__init__()
        global x, y

        self.eventName = eventName
        self.active = active
        print(args, kwargs)
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


class GameMenu(Scene):

    is_event_handler = True

    def __init__(self):
        super().__init__()
        global title
        title.x = reswidth * 0.13
        title.y = resheight * 0.94
        self.add(title)
        backButton = mediumButton("BACK", events.mainmenuevents.backToMainMenu)
        backButton.x = reswidth * 0.065
        backButton.y = resheight * 0.89
        backButton.show(0.01)
        self.add(backButton)
        events.gamemenuevents.push_handlers(self)
        modeBoxes = []
        for modeName, mode in modes.gamemodes.items():
            modeBox = GameModeBox(mode)
            modeBoxes.append(modeBox)
        for i in range(len(modeBoxes)):
            modeBoxes[i].x = ((reswidth * 0.8) // 4) * (((i + 1) / 4) - ((i) // 4)) * 4
            modeBoxes[i].y = resheight * (0.6 - (i // 4) * 0.47)
            modeBoxes[i].delay = 2 + i
            modeBoxes[i].update_positions()
            extendedInfo = ExtendedInfo(modeBoxes[i].gameMode)
            self.add(modeBoxes[i], z=1)
            self.add(extendedInfo, z=2)
            for child in modeBoxes[i].get_children():
                if isinstance(child, smallButton):
                    child.do(Delay(modeBoxes[i].delay / 4) + CallFunc(child.show))
                else:
                    child.do(FadeOut(0.01) + Delay(modeBoxes[i].delay / 4) + FadeIn(0.5))

    def on_enter(self):
        super().on_enter()

    def gameModeChosen(self, chosenGameMode):
        pass


class GameModeBox(Layer):

    def __init__(self, gameMode):
        super().__init__()
        self.gameMode = gameMode
        self.bg = Sprite("gameBox.png")
        self.thumbnail = Sprite(gameMode.thumbnail)
        self.thumbnail.scale_x = 200 / self.thumbnail.width
        self.thumbnail.scale_y = 200 / self.thumbnail.height
        self.infoButton = smallButton("i", events.gamemenuevents.showExtendedInfo, eventparam=gameMode.name)
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
    
    def update_positions(self):
        self.thumbnail.x = 0
        self.thumbnail.y = 20
        self.gmTitle.x = -100
        self.gmTitle.y = -104
        self.infoButton.x = 80
        self.infoButton.y = -107
        self.infoButton.px = self.x
        self.infoButton.py = self.y
        

class ExtendedInfo(Layer):

    is_event_handler = True
    
    def __init__(self, gameMode):
        super().__init__()
        events.gamemenuevents.push_handlers(self)
        self.gameMode = gameMode
        self.infoBox = Sprite("infoBox.png")
        self.bgDimmer = ColorLayer(0, 0, 0, 20)
        self.exitButton = smallButton("X", events.gamemenuevents.hideExtendedInfo, eventparam=self.gameMode.name)
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
        self.thumbnail.x = reswidth * 0.3
        self.thumbnail.y = resheight / 2
        self.title = Label(gameMode.name, anchor_x="center", anchor_y="center", font_size=39, color=(0, 0, 0, 255))
        self.title.x = reswidth * 0.65
        self.title.y = resheight * 0.75
        self.desc = Label(gameMode.desc, anchor_x="center", anchor_y="top", font_size=17, multiline = True, width=(x * 0.36), height=(y * 0.2), color=(0, 0, 0, 255))
        self.desc.x = reswidth * 0.65
        self.desc.y = resheight * 0.65
        self.add(self.infoBox, z=5)
        self.add(self.bgDimmer, z=4)
        self.add(self.exitButton, z=5)
        self.add(self.thumbnail, z=5)
        self.add(self.title, z=5)
        self.add(self.desc, z=5)
        self.bgDimmer.do(FadeOut(0.01))
        self.infoBox.do(FadeOut(0.01))
        self.exitButton.hide(0.01)
        self.thumbnail.do(FadeOut(0.01))
        self.title.do(FadeOut(0.01))
        self.desc.do(FadeOut(0.01))
        
       
    def ExtendedInfoShow(self, name):
        if name == self.gameMode.name and not self.active:
            self.infoBox.do(FadeIn(0.5))
            self.bgDimmer.do(FadeTo(150, 0.5))
            self.thumbnail.do(FadeIn(0.5))
            self.title.do(FadeIn(0.5))
            self.desc.do(FadeIn(0.5))
            self.exitButton.show()
            self.active = True
    
    def ExtendedInfoHide(self, name):
        if name == self.gameMode.name and self.active:
            self.infoBox.do(FadeOut(0.5))
            self.bgDimmer.do(FadeTo(0, 0.5))
            self.thumbnail.do(FadeOut(0.5))
            self.title.do(FadeOut(0.5))
            self.desc.do(FadeOut(0.5))
            self.exitButton.hide()
            self.active = False