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
from elements import * 
from scroll import *

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

class LevelMenu(Scene):

    is_event_handler = True
    
    def __init__(self):
        super().__init__()
        events.gamemenuevents.push_handlers(self)
        global title
        self.levelTitle = title
        self.levelTitle.element.text = "Levels"
        self.levelTitle.x = reswidth * 0.13
        self.levelTitle.y = resheight * 1.2
        backButton = mediumButton("BACK", events.mainmenuevents.backToMainMenu)
        backButton.x = reswidth * 0.065
        backButton.y = resheight * 0.89
        backButton.show(0.01)
        newButton = mediumButton("NEW", events.mainmenuevents.backToMainMenu) # TODO: Need to change to level creator/editor
        newButton.x = reswidth * 0.935
        newButton.y = resheight * 0.89
        newButton.show(0.01)
        self.chosenBox = ChosenBox(cfg.loadedGameMode)
        self.chosenBox.x = reswidth * 0.7
        self.chosenBox.y = resheight * 1.2
        self.chosenBox.update_positions()
        self.add(self.chosenBox)
        self.add(backButton)
        self.add(newButton)
        self.add(self.levelTitle)
        self.levelTitle.do(AccelDeccel(MoveTo((self.levelTitle.x, resheight * 0.94), 2)))
        self.chosenBox.do(AccelDeccel(MoveTo((self.chosenBox.x, resheight * 0.89), 2)))
        self.playButton = mediumButton("PLAY!", events.gamemenuevents.onPlayButtonClick)
        self.playButton.x = reswidth * 0.9
        self.playButton.y = resheight * -0.1
        self.add(self.playButton)
        self.playButton.show()

        blackLayer = layer.ColorLayer(0, 0, 0, 255)
        blackLayer.width = reswidth
        blackLayer.height = int(resheight * 0.35)
        blackLayer.x = 0
        blackLayer.y = int(resheight - (blackLayer.height / 2))
        self.add(blackLayer, z = -1)

        self.scrollManager = layer.ScrollingManager()
        self.scrollBar = ScrollBar(self.scrollManager)
        self.scrollLayer = ScrollLayer(reswidth/2, resheight, reswidth, resheight, self.scrollBar)
        
        self.scrollLayer.x = 0
        self.scrollLayer.y = 0

        self.scrollBar.x = reswidth - (self.scrollBar.width / 2)
        self.scrollBar.y = (resheight - (resheight * 0.02)) - (self.scrollBar.img.height / 2)

        self.levelBoxes = []
        if len(levels.levels) == 0:
            warningLbl = Label("There were no levels loaded.", position=(reswidth/2, resheight/2), font_size=20, anchor_x="center", anchor_y="center")
            self.add(warningLbl)
            warningLbl.do(FadeOut(0.00001) + Delay(1) + FadeIn(1))
        else:
            for levelName, level in levels.levels.items():
                levelBox = LevelBox(level, scrollManager=self.scrollManager)
                self.levelBoxes.append(levelBox)
            for i in range(len(self.levelBoxes)):
                self.levelBoxes[i].x = ((reswidth * 0.8) // 4) * (((i + 1) / 4) - ((i) // 4)) * 4
                self.levelBoxes[i].y = resheight * (0.6 - (i // 4) * 0.47)
                self.levelBoxes[i].delay = 2 + i
                self.levelBoxes[i].update_positions()
                extendedInfo = LVLExtendedInfo(self.levelBoxes[i].level)
                self.scrollLayer.add(self.levelBoxes[i], z=1)
                self.add(extendedInfo, z=2)
                self.levelBoxes[i].show()        

        self.scrollManager.add(self.scrollLayer)
        self.scrollLayer.calculate()
        self.scrollManager.set_focus(reswidth / 2, resheight / 2)

        self.add(self.scrollManager, z = -2)
        self.add(self.scrollBar)

        if len(self.levelBoxes) < 5:
            self.scrollBar.showing = False


    def LevelChosen(self, level):
        self.playButton.do(AccelDeccel(MoveTo((self.playButton.x, resheight * 0.1), duration = 2)))
        levels.levelLoad(level.idx)

    
    def ChosenBoxClicked(self):
        self.chosenBox.do(Accelerate(MoveTo((self.chosenBox.x, resheight * 1.2), 1), rate = 3.5))
        for i in range(len(self.levelBoxes)):
            self.levelBoxes[i].hide(1)
        self.levelTitle.do(Accelerate(MoveTo((self.levelTitle.x, resheight * 1.2), 1), rate = 3.5) + CallFunc(events.gamemenuevents.onReturnToGMMenu))


class GameModeMenu(Scene):

    is_event_handler = True

    def __init__(self):
        super().__init__()
        global title
        self.gamemodeTitle = title
        self.gamemodeTitle.element.text = "Game Modes"
        self.gamemodeTitle.x = reswidth * 0.13
        self.gamemodeTitle.y = resheight * 0.94
        self.add(self.gamemodeTitle)
        backButton = mediumButton("BACK", events.mainmenuevents.backToMainMenu)
        backButton.x = reswidth * 0.065
        backButton.y = resheight * 0.89
        backButton.show(0.01)
        newButton = mediumButton("NEW", events.mainmenuevents.backToMainMenu) # TODO: Need to change to level creator/editor
        newButton.x = reswidth * 0.935
        newButton.y = resheight * 0.89
        newButton.show(0.01)
        
        self.add(backButton)
        self.add(newButton)
        events.gamemenuevents.push_handlers(self)

        blackLayer = layer.ColorLayer(0, 0, 0, 255)
        blackLayer.width = reswidth
        blackLayer.height = int(resheight * 0.35)
        blackLayer.x = 0
        blackLayer.y = int(resheight - (blackLayer.height / 2))
        self.add(blackLayer, z = -1)

        self.scrollManager = layer.ScrollingManager()
        self.scrollBar = ScrollBar(self.scrollManager)
        self.scrollLayer = ScrollLayer(reswidth/2, resheight, reswidth, resheight, self.scrollBar)
        
        self.scrollLayer.x = 0
        self.scrollLayer.y = 0

        self.scrollBar.x = reswidth - (self.scrollBar.width / 2)
        self.scrollBar.y = (resheight - (resheight * 0.02)) - (self.scrollBar.img.height / 2)

        self.modeBoxes = []
        if len(modes.gamemodes) == 0:
            warningLbl = Label("There were no game modes loaded.", position=(reswidth/2, resheight/2), font_size=20, anchor_x="center", anchor_y="center")
            self.add(warningLbl)
        else:
            for modeName, mode in modes.gamemodes.items():
                modeBox = GameModeBox(mode, scrollManager = self.scrollManager)
                self.modeBoxes.append(modeBox)
            for i in range(len(self.modeBoxes)):
                self.modeBoxes[i].x = ((reswidth * 0.8) // 4) * (((i + 1) / 4) - ((i) // 4)) * 4
                self.modeBoxes[i].y = resheight * (0.6 - (i // 4) * 0.47)
                self.modeBoxes[i].delay = 2 + i
                self.modeBoxes[i].update_positions()
                extendedInfo = GMExtendedInfo(self.modeBoxes[i].gameMode)
                self.scrollLayer.add(self.modeBoxes[i], z=1)
                self.add(extendedInfo, z=2)
                self.modeBoxes[i].show()


        self.scrollManager.add(self.scrollLayer)
        self.scrollLayer.calculate()
        self.scrollManager.set_focus(reswidth / 2, resheight / 2)

        self.add(self.scrollManager, z = -2)
        self.add(self.scrollBar)

        if len(self.modeBoxes) < 5:
            self.scrollBar.showing = False

    def on_enter(self):
        super().on_enter()

    def GameModeChosen(self, chosenGameMode):
        for i in range(len(self.modeBoxes)):
            if chosenGameMode == self.modeBoxes[i].gameMode:
                self.modeBoxes[i].chosen = True
                modes.loadGameMode(modes.gamemodes[self.modeBoxes[i].gameMode.idx])
                self.do(Delay(1) + CallFunc(self.modeBoxes[i].hide))
                self.gamemodeTitle.do(Delay(1) + Accelerate(MoveTo((self.gamemodeTitle.x, resheight * 1.2), 1), rate = 3.5) + CallFunc(events.gamemenuevents.onReplaceGMMenu))

            else:
                self.modeBoxes[i].hide()

    def ReturnToGMMenu(self):
        self.gamemodeTitle.y = resheight * 1.2
        self.gamemodeTitle.do(AccelDeccel(MoveTo((self.gamemodeTitle.x, resheight * 0.94), 2)))



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
        self.height_range = [int((self.y) - (self.bg.height / 2)), int((self.y) + (self.bg.height / 2))]

        self.schedule_interval(self.setWH, 1)
        self.resume_scheduler()

    def update_positions(self):
        self.gmTitle.x = -200
        self.gmTitle.y = -15

    def setWH(self, dt):
        x, y = director.window.width, director.window.height
        nmin = sc.scale(int((self.x) - (self.bg.width / 2)), int((self.y) - (self.bg.height / 2)))
        nmax = sc.scale(int((self.x) + (self.bg.width / 2)), int((self.y) + (self.bg.height / 2)))
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

    def __init__(self, level, scrollManager = None):
        super().__init__()
        events.gamemenuevents.push_handlers(self)
        self.level = level
        self.bg = Sprite("gameBox.png")
        self.thumbnail = Sprite(level.thumbnail)
        self.thumbnail.scale_x = 200 / self.thumbnail.width
        self.thumbnail.scale_y = 200 / self.thumbnail.height
        self.infoButton = scrollSmallButton("i", events.gamemenuevents.showExtendedInfo, eventparam=level.idx, scrollManager=scrollManager)
        self.scrollManager = scrollManager
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
        self.height_range = [int((self.y) - (self.bg.height / 2)), int((self.y) + (self.bg.height / 2))]

        self.schedule(self.setWH)
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
        nmax = sc.scale(int((self.x) + (self.bg.width / 2)), int((self.y) + (self.bg.height / 2)))
        if not self.scrollManager == None:
            nmin = [nmin[0], (nmin[1] + self.scrollManager.get_children()[0].y)]
            nmax = [nmax[0], (nmax[1] + self.scrollManager.get_children()[0].y)]
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
        self.do(Delay(1) + CallFunc(self.ExtendedInfoHide2))

    def ExtendedInfoHide2(self):
        self.showing = True

class LVLExtendedInfo(layer.Layer):

    is_event_handler = True
    
    def __init__(self, level):
        super().__init__()
        events.gamemenuevents.push_handlers(self)
        self.level = level
        self.infoBox = Sprite("infoBox.png")
        self.bgDimmer = layer.ColorLayer(0, 0, 0, 20)
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

class scrollSmallButton(smallButton):

    def __init__(self, label, eventName, active=False, scrollManager = None, *args, **kwargs):
        super().__init__(label, eventName, active=active, *args, **kwargs)
        self.scrollManager = scrollManager

    def setWH(self, dt):
        x, y = director.window.width, director.window.height
        nmin = sc.scale(int((self.px + self.x) - (self.bgImage.width / 2)), int((self.py + self.y) - (self.bgImage.height / 2)))
        nmax = sc.scale(int((self.px + self.x) + (self.bgImage.width / 2)), int((self.py + self.y) + (self.bgImage.height / 2)))
        if not self.scrollManager == None:
            nmin = [nmin[0], (nmin[1] + self.scrollManager.get_children()[0].y)]
            nmax = [nmax[0], (nmax[1] + self.scrollManager.get_children()[0].y)]
        self.width_range = [int(nmin[0]), int(nmax[0])]
        self.height_range = [int(nmin[1]), int(nmax[1])]

class GameModeBox(layer.Layer):

    is_event_handler = True

    def __init__(self, gameMode, scrollManager = None):
        super().__init__()
        events.gamemenuevents.push_handlers(self)
        self.gameMode = gameMode
        self.bg = Sprite("gameBox.png")
        self.thumbnail = Sprite(gameMode.thumbnail)
        self.thumbnail.scale_x = 200 / self.thumbnail.width
        self.thumbnail.scale_y = 200 / self.thumbnail.height
        self.infoButton = scrollSmallButton("i", events.gamemenuevents.showExtendedInfo, eventparam=gameMode.idx, scrollManager=scrollManager)
        self.width = self.bg.width
        self.height = self.bg.height
        self.scrollManager = scrollManager
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
        self.height_range = [int((self.y) - (self.bg.height / 2)), int((self.y) + (self.bg.height / 2))]

        self.schedule(self.setWH)
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
        nmin = int((self.x) - (self.bg.width / 2)), int((self.y) - (self.bg.height / 2))
        nmax = int((self.x) + (self.bg.width / 2)), int((self.y) + (self.bg.height / 2))
        if not self.scrollManager == None:
            nmin = [nmin[0], (nmin[1] + self.scrollManager.get_children()[0].y)]
            nmax = [nmax[0], (nmax[1] + self.scrollManager.get_children()[0].y)]
        nmin = sc.scale(nmin[0], nmin[1])
        nmax = sc.scale(nmax[0], nmax[1])
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
        self.do(Delay(1) + CallFunc(self.ExtendedInfoHide2))

    def ExtendedInfoHide2(self):
        self.showing = True

class GMExtendedInfo(layer.Layer):

    is_event_handler = True
    
    def __init__(self, gameMode):
        super().__init__()
        events.gamemenuevents.push_handlers(self)
        self.gameMode = gameMode
        self.infoBox = Sprite("infoBox.png")
        self.bgDimmer = layer.ColorLayer(0, 0, 0, 20)
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
