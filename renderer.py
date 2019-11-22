import cocos
import logger
from cocos.text import Label
from cocos import scene
from cocos import layer
from cocos.actions import *
from cocos.director import director
from cocos import pyglet
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


class Events(pyglet.window.EventDispatcher):
    def __init__(self):
        super(Events, self).__init__()
    
class BaseWindow(scene.Scene):

    def __init__(self):
        super(BaseWindow, self).__init__()

class loadingScreen(BaseWindow):

    is_event_handler = True

    def __init__(self):
        super(loadingScreen, self).__init__()
        x, y = cocos.director.director.get_window_size()
        title.position = x / 2, y * 0.72
        self.add(title)
        title.do(FadeIn(1))
        self.startProgress()

    def startProgress(self):
        self.initResources() 
        self.progressFinish()

    def progress(self):
        #progressBar.do()
        pass

    def progressFinish(self):
        print("progressFinish()")
        director.replace(MainMenu)

    def initResources(self):
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
        self.add(label2)
        print("NEw scene loaded")

if __name__=="__main__":
    print("This file cannot be run directly, please run main.py to start the game.")