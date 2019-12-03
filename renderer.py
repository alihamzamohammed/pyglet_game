import cocos
import logger
from cocos.text import Label
from cocos import scene
from cocos import layer
from cocos.actions import *
from cocos.director import director
import events
import pyglet
from pyglet import event
import resources

titleLabel = cocos.text.Label(
    "Game Title",
    font_name=resources.font[1],
    font_size=40,
    anchor_y="top",
    anchor_x="center"
)
title = layer.Layer()
title.add(titleLabel)

class RendererEvents(pyglet.window.EventDispatcher):

    def __init__(self):
        super(RendererEvents, self).__init__()

    def onProgressFinished(self):
        print("Event dispatching!")
        self.dispatch_event("progressFinished")
        print("Event dispatched!")
    
RendererEvents.register_event_type("progressFinished")

class BaseWindow(scene.Scene):

    def __init__(self):
        super(BaseWindow, self).__init__()

class MainMenu(BaseWindow):

    is_event_handler = True

    def __init__(self):
        super(MainMenu, self).__init__()
        #self.add(title)
        #x, y = cocos.director.director.get_window_size()
        #title.do(MoveTo(x / 2, y * 0.9), duration=4)
        label2 = Label(
            "test1"
        )
        label2.position = 100, 100
        self.add(label2)
        print("New scene loaded")

class loadingScreen(BaseWindow):

    is_event_handler = True

    def __init__(self):
        super(loadingScreen, self).__init__()
        x, y = cocos.director.director.get_window_size()
        evts = RendererEvents()
        title.position = x / 2, y * 0.72
        self.add(title)
        title.do(FadeIn(1))      
        logger.addLog("Init levels", logger.loglevel["info"])
        # check to see if all levels are in level db, otherwise raise warning, and do not load
        # Render level thumbnails, and put them as sprite objects into array
        logger.addLog("Init game modes", logger.loglevel["info"])
        # check to see if all game modes exist in game mode db
        # render game mode metadata and add to multidimensional array dict
        logger.addLog("Init resources", logger.loglevel["info"])
        # complete
        logger.addLog("Init items", logger.loglevel["info"])
        # check to see if all item packs are in item pack db, and if all item xml is without error
        # add item packs and individual items to multidimensional array
        evts.onProgressFinished()
        

if __name__=="__main__":
    print("This file cannot be run directly, please run main.py to start the game.")