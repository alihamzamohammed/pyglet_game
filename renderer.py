import cocos
import logger
from cocos.text import Label
from cocos import scene
from cocos import layer
from cocos.actions import *
from cocos.menu import *
from cocos.director import director
import events
import pyglet
import threading
from pyglet import event
import resources

'''Game loading code'''
def game_loading():
    logger.addLog("Starting game loading!", logger.loglevel["info"])
    # Start loading, dispatch events when aspect of loading completed
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
    events.rendererevents.onProgressFinished()


'''Elements of windows'''
titleLabel = cocos.text.Label(
    "Game Title",
    font_name=resources.font[1],
    font_size=40,
    anchor_y="top",
    anchor_x="center"
)

class MainMenu(Menu):

    def __init__(self, title=""):
        super().__init__(title=title)
        #self.title_label = Label("")
        x, y = cocos.director.director.get_window_size()
        menuitems = []
        menuitems.append(MenuItem("Play", self.play))
        menuitems.append(MenuItem("Multiplayer", self.multiplayer))
        menuitems.append(MenuItem("Settings", self.settings))
        menuitems.append(MenuItem("Quit Game", self.quit))
        self.create_menu(menuitems, zoom_in(), zoom_out())
        
    def play(self):
        pass

    def multiplayer(self):
        pass

    def settings(self):
        pass

    def quit(self):
        pass


'''Game scenes'''
class BaseWindow(scene.Scene):
    def __init__(self):
        super(BaseWindow, self).__init__()


class MainMenuScreen(BaseWindow):
    is_event_handler = True

    def __init__(self):
        super(MainMenuScreen, self).__init__()
        x, y = cocos.director.director.get_window_size()
        self.add(titleLabel)
        titleLabel.do(AccelDeccel(MoveTo((x / 2, y * 0.85), 2)))
        self.add(MainMenu(""))


class loadingScreen(BaseWindow):
    is_event_handler = True

    def __init__(self):
        super(loadingScreen, self).__init__()
        x, y = cocos.director.director.get_window_size()
        titleLabel.position = x / 2, y * 0.72
        self.add(titleLabel)
        titleLabel.do(FadeIn(1))
        loadingThread = threading.Thread(target=game_loading)
        loadingThread.start()

if __name__=="__main__":
    print("This file cannot be run directly, please run main.py to start the game.")