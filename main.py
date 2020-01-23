import os
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
director.init(width=reswidth, height=resheight, caption="Game", fullscreen=fullscreen, autoscale=True, resizable=False)
    
import resources
resources.resourceLoad() 

import renderer

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
        director.replace(FadeTransition(renderer.SettingsScreen(), duration = 5, color = (0, 0, 0)))
        print("Settings button clicked")

    def quitButtonClicked(self):
        print("Quit button clicked")

    def __init__(self):
        super(Game, self).__init__()
        events.rendererevents.push_handlers(self)

if __name__=="__main__":
    logger.addLog("Starting game.", logger.loglevel["info"])
    game = Game()
    game.startGame()