import cocos
import logger
from cocos.text import Label
from cocos import scene
from cocos import layer
from cocos.actions import *
from cocos.director import director
import events
import pyglet
import threading
from pyglet import event
import resources


class BaseWindow(scene.Scene):

    def __init__(self):
        super(BaseWindow, self).__init__()

def game_loading():
    print("Game loading start")
    logger.addLog("Init levels", logger.loglevel["info"])
    print(cocos.director.director.scene)
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
    events.rendererevents.onProgressFinished()

class MainMenu(BaseWindow):

    is_event_handler = True

    def __init__(self):
        super(MainMenu, self).__init__()


class loadingScreen(BaseWindow):

    is_event_handler = True

    def __init__(self):
        super(loadingScreen, self).__init__()
        titleLabel = cocos.text.Label(
            "Game Title",
            font_name=resources.font[1],
            font_size=40,
            anchor_y="top",
            anchor_x="center"
        )
        title = layer.Layer()
        x, y = cocos.director.director.get_window_size()
        title.position = x / 2, y * 0.72
        title.add(titleLabel)
        self.add(title)
        title.do(FadeIn(1))
        loadingThread = threading.Thread(target=game_loading)
        loadingThread.start()
        print("Thread start called")
        
def get_scene(scene):
    if scene == "loadingScreen":
        return loadingScreen()
    elif scene == "MainMenu":
        return MainMenu()

if __name__=="__main__":
    print("This file cannot be run directly, please run main.py to start the game.")