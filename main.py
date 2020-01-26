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

reswidth, resheight = [int(res) for res in cfg.configuration["Core"]["defaultres"].split("x")]
fullscreen = True if cfg.configuration["Core"]["fullscreen"] == "True" else False
vsync = True if cfg.configuration["Core"]["vsync"] == True else False
director.init(width=reswidth, height=resheight, caption="Game", fullscreen=fullscreen, autoscale=True, resizable=True, vsync=vsync)
    
import resources
resources.resourceLoad() 

import renderer
import settings

class Game(object):
    
    is_event_handler = True
    
    def startGame(self):
        logger.addLog("Resolution is " + str(reswidth) + "x" + str(resheight), logger.loglevel["info"])
        if fullscreen == True:
            logger.addLog("Fullscreen is enabled", logger.loglevel["info"])
        else:
            logger.addLog("Fullscreen is disabled", logger.loglevel["info"])
        director.run(renderer.loadingScreen())

    def progressFinished(self):
        logger.addLog("Loading finished, displaying Main Menu", logger.loglevel["info"])
        director.replace(renderer.MainMenuScreen())

    def playButtonClicked(self):
        print("Play button clicked")

    def multiplayerButtonClicked(self):
        print("Multiplayer button clicked")

    def settingsButtonClicked(self):
        director.replace(FadeTransition(settings.SettingsScreen(), duration = 1, color = (0, 0, 0)))
        print("Settings button clicked")

    def quitButtonClicked(self):
        sys.exit()

    def showMainMenu(self):
        cfg.configWrite(defaultconfigfile)
        director.replace(FadeTransition(renderer.MainMenuScreen(), duration = 1, color = (0, 0, 0)))

    def __init__(self):
        super(Game, self).__init__()
        events.rendererevents.push_handlers(self)

if __name__=="__main__":
    logger.addLog("Starting game.", logger.loglevel["info"])
    game = Game()
    game.startGame()