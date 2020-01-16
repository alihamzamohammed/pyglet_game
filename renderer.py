import cocos
import logger
from cocos.text import Label
from cocos import scene
from cocos import layer
from cocos.actions import *
from cocos.menu import *
from cocos.sprite import *
from cocos.director import director
import events
import pyglet
import pyglet.gl
import threading
from pyglet import event
import resources
import time

x, y = director.get_window_size()

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

class mainMenu(layer.ColorLayer):

    # class MenuItem(layer.Layer):

    #     is_event_handler = True

    #     def __init__(self, label, callbackfunc):
    #         super().__init__()
    #         global x, y
    #         self.callbackfunc = callbackfunc
    #         bgImage = Sprite("image.png") # Replace with resource pack image
    #         self.lbl  = Label(label)
    #         bgImage.anchor_x = x / 2
    #         bgImage.anchor_y = y / 2
    #         self.add(bgImage, z=0)
    #         self.add(self.lbl, z=0)
    #         self.width_range = bgImage.x, bgImage.x + bgImage.width
    #         self.height_range = bgImage.y, bgImage.y + bgImage.height

    #     def on_mouse_motion(self, x, y):
    #         if x in range(self.width_range) and y in range(self.height_range):
    #             #self.callbackfunc()
    #             self.lbl.element.text = "Hovered"

    def __init__(self):
        global x, y
        super().__init__(100, 100, 100, 0, width=int(x * 0.4), height=int(y * 0.55))
        #self.add(MenuItem("hello", self.play))
        

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


""" class MainMenuLayer(layer.Layer):

    def __init__(self):
        super().__init__()

    def on_enter(self):
        super().on_enter()
        self.add(MainMenu(), z=1)
        self.do(Delay(2) + FadeIn(1))
 """

class MainMenuScreen(BaseWindow):
    is_event_handler = True

    def __init__(self):
        super(MainMenuScreen, self).__init__()
        global x, y
        self.add(titleLabel)
        titleLabel.do(AccelDeccel(MoveTo((x / 2, y * 0.85), 2)))
        mainmenu = mainMenu()
        mainmenu.position = (x / 2) - (mainmenu.width / 2), (y * 0.4) - (mainmenu.height / 2)
        self.add(mainmenu)
        mainmenu.do(Delay(1) + FadeIn(2))


class loadingScreen(BaseWindow):
    is_event_handler = True

    def __init__(self):
        super(loadingScreen, self).__init__()
        x, y = cocos.director.director.get_window_size()
        titleLabel.position = x / 2, y * 0.72
        self.add(titleLabel)
        titleLabel.do(FadeIn(1))

    def on_enter(self):
        super().on_enter()
        game_loading()

if __name__=="__main__":
    print("This file cannot be run directly, please run main.py to start the game.")