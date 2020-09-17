import os
import sys
import pyglet
import cocos
from cocos.director import director
from cocos.scene import *
from cocos.scenes import *
from pyglet import event
import events
import cfg
cfg.init()
defaultconfigfile = "settings.ini"
cfg.configRead(defaultconfigfile)
import time
import logger
logger.init()

reswidth, resheight = [int(res) for res in cfg.resolution.split("x")]
fullscreen = True if cfg.configuration["Core"]["fullscreen"] == "True" else False
vsync = True if cfg.configuration["Core"]["vsync"] == "True" else False
showfps = True if cfg.configuration["Core"]["showfps"] == "True" else False
director.init(width=reswidth, height=resheight, caption="Game", fullscreen=fullscreen, autoscale=True, resizable=True, vsync=vsync)
director.set_show_FPS(showfps)

logger.addLog("Init resources", logger.loglevel["debug"])
import resources
resources.resourceLoad()


import mainmenu
import gamemenu
import settings

import renderer
renderer.init()

import levels
import items
import modes

class Game(object):

    is_event_handler = True

    def startGame(self):
        logger.addLog("Resolution is " + str(reswidth) + "x" + str(resheight), logger.loglevel["debug"])
        if fullscreen:
            logger.addLog("Fullscreen is enabled", logger.loglevel["debug"])
        else:
            logger.addLog("Fullscreen is disabled", logger.loglevel["debug"])
        director.run(mainmenu.loadingScreen())

    def progressFinished(self):
        logger.addLog("Loading finished, displaying Main Menu", logger.loglevel["debug"])
        director.replace(FadeTransition(mainmenu.MainMenuScreen(), duration = 0.001))

    def playButtonClicked(self):
        # DEBUG: Debug code, not for final version
        #lvl = levels.levelLoad("test")
        #director.replace(FadeTransition(renderer.Renderer(lvl, modes.loadGameMode(modes.gamemodes["freeplay"])), duration = 1))
        print("Play button clicked")
        director.replace(FadeTransition(gamemenu.GameModeMenu(), duration = 1, color = (0, 0, 0)))

    def multiplayerButtonClicked(self):
        print("Multiplayer button clicked")
        logger.addLog("Multiplayer not yet implemented!")

    def settingsButtonClicked(self):
        director.replace(FadeTransition(settings.SettingsScreen(), duration = 1, color = (0, 0, 0)))
        print("Settings button clicked")

    def quitButtonClicked(self):
        director.terminate_app = True

    def showMainMenu(self):
        global defaultconfigfile
        cfg.configWrite(defaultconfigfile)
        director.replace(FadeTransition(mainmenu.MainMenuScreen(), duration = 1, color = (0, 0, 0)))
        cfg.loadedLevel = None
        cfg.loadedGameMode = None

    def replaceLevelMenu(self):
        director.replace(FadeTransition(gamemenu.LevelMenu(), duration = 0.001))

    def __init__(self):
        super(Game, self).__init__()
        events.mainmenuevents.push_handlers(self)
        events.gamemenuevents.push_handlers(self)

if __name__=="__main__":
    logger.addLog("Starting game.", logger.loglevel["debug"])
    game = Game()
    game.startGame()