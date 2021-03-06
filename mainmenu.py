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

x, y = director.window.width, director.window.height
reswidth, resheight = [int(res) for res in cfg.resolution.split("x")]

'''Game loading code'''
def game_loading():
    logger.addLog("Starting game loading!", logger.loglevel["debug"])
    # Start loading, dispatch events when aspect of loading completed

    logger.addLog("Init items", logger.loglevel["debug"])
    # check to see if all item packs are in item pack db, and if all item xml is without error
    # add item packs and individual items to multidimensional array
    import items
    items.init()

    logger.addLog("Init levels", logger.loglevel["debug"])
    # check to see if all levels are in level db, otherwise raise warning, and do not load
    # Render level thumbnails, and put them as sprite objects into array
    import levels
    levels.init()

    logger.addLog("Init game modes", logger.loglevel["debug"])
    # check to see if all game modes exist in game mode db
    # render game mode metadata and add to multidimensional array dict
    import modes
    modes.init()
    

    events.mainmenuevents.onProgressFinished()


'''Elements of windows'''
gameTitle = elements.titleLabel
gameTitle.element.text = "Game Title"


'''Game scenes'''
class MainMenuScreen(scene.Scene):

    is_event_handler = True

    def __init__(self):
        super(MainMenuScreen, self).__init__()
        global x, y
        self.add(gameTitle)
        self.do(Delay(1) + CallFunc(events.mainmenuevents.mainMenuShowing))
        gameTitle.do(AccelDeccel(MoveTo((x / 2, y * 0.9), 1.5)))

        playButton = elements.MainMenuButton("Play Game", events.mainmenuevents.onPlayButtonClick, 1)
        multiplayerButton = elements.MainMenuButton("Multiplayer", events.mainmenuevents.onMultiplayerButtonClick, 2)
        settingsButton = elements.MainMenuButton("Settings", events.mainmenuevents.onSettingsButtonClick, 3)
        quitButton = elements.MainMenuButton("Quit Game", events.mainmenuevents.onQuitButtonClicked, 4)

        self.add(playButton)
        self.add(multiplayerButton)
        self.add(settingsButton)
        self.add(quitButton)


class loadingScreen(scene.Scene):

    is_event_handler = True

    def __init__(self):
        super(loadingScreen, self).__init__()
        x, y = cocos.director.director.get_window_size()
        self.loaded = False
        gameTitle.position = x / 2, y * 0.7
        self.add(gameTitle)
        gameTitle.do(FadeIn(1))

    def on_enter(self):
        super().on_enter()
        if not self.loaded:
            game_loading()
            self.loaded = True

if __name__=="__main__":
    print("This file cannot be run directly, please run main.py to start the game.")