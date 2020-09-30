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
        self.levelBoxes = []
        for levelName, level in levels.levels.items():
            levelBox = LevelBox(level)
            self.levelBoxes.append(levelBox)
        for i in range(len(self.levelBoxes)):
            self.levelBoxes[i].x = ((reswidth * 0.8) // 4) * (((i + 1) / 4) - ((i) // 4)) * 4
            self.levelBoxes[i].y = resheight * (0.6 - (i // 4) * 0.47)
            self.levelBoxes[i].delay = 2 + i
            self.levelBoxes[i].update_positions()
            extendedInfo = LVLExtendedInfo(self.levelBoxes[i].level)
            self.add(self.levelBoxes[i], z=1)
            self.add(extendedInfo, z=2)
            self.levelBoxes[i].show()

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
        self.modeBoxes = []
        for modeName, mode in modes.gamemodes.items():
            modeBox = GameModeBox(mode)
            self.modeBoxes.append(modeBox)
        for i in range(len(self.modeBoxes)):
            self.modeBoxes[i].x = ((reswidth * 0.8) // 4) * (((i + 1) / 4) - ((i) // 4)) * 4
            self.modeBoxes[i].y = resheight * (0.6 - (i // 4) * 0.47)
            self.modeBoxes[i].delay = 2 + i
            self.modeBoxes[i].update_positions()
            extendedInfo = GMExtendedInfo(self.modeBoxes[i].gameMode)
            self.add(self.modeBoxes[i], z=1)
            self.add(extendedInfo, z=2)
            self.modeBoxes[i].show()

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

