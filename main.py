import os
import cocos
from cocos.director import director
from cocos.scene import *
import pyglet
from pyglet import event
import events
import cfg
import threading
cfg.init()
defaultconfigfile = "settings.ini"
cfg.configRead(defaultconfigfile)

import logger
logger.init()

reswidth, resheight = [int(res) for res in cfg.configuration["Core"]["defaultres"].split("x")]
fullscreen = True if cfg.configuration["Core"]["fullscreen"] == "True" else False
director.init(width=reswidth, height=resheight, caption="Game", fullscreen=fullscreen, autoscale=True)
    
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
        print(director)
        director.run(renderer.get_scene("loadingScreen"))

    def progressFinished(self):
        print("Event registered, switching scenes!")
        #t1 = threading.Thread
        director.replace(renderer.get_scene("MainMenu"))
        print(director.scene)

    def __init__(self):
        super(Game, self).__init__()
        events.rendererevents.push_handlers(self)

if __name__=="__main__":
    logger.addLog("Starting game.", logger.loglevel["info"])
    game = Game()
    game.startGame()