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
import random
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
    font_size=50,
    anchor_y="top",
    anchor_x="center"
)

class mainMenu(layer.ColorLayer):

    class menuItem(layer.Layer):
        
        is_event_handler = True
        
        def __init__(self, label, callbackfunc, posx, posy):
            super().__init__()
            global x, y
            self.callbackfunc = callbackfunc
            bgImage = Sprite("image.png") # Replace with resource pack image
            lbl = Label(label)
            #bgImage.anchor_x = x / 2
            #bgImage.anchor_y = y / 2
            self.add(bgImage, z=0)
            self.add(lbl, z=1)
            self.anchor = (0, 0)
            self.x = posx
            self.y = posy
            self.width = bgImage.width
            self.height = bgImage.height
            self.width_range = [int(self.x), int(self.x + self.width)]
            self.height_range = [int(self.y), int(self.y + self.height)]
            print(self.width_range)
            print(self.height_range)
        
        def on_mouse_motion(self, x, y, dx, dy):
            if x in range(self.width_range[0], self.width_range[1]) and y in range(self.height_range[0], self.height_range[1]):
                #self.callbackfunc()
                #self.lbl.element.text = "Hovered"
                #print("hovering over button" + str(random.randint(1, 100)))
                print(x, y)

    def __init__(self):
        global x, y
        super().__init__(100, 100, 100, 0, width=int(x * 0.4), height=int(y * 0.6))
        self.x = (x / 2) - (self.width / 2)
        self.y = (y * 0.42) - (self.height / 2)
        print(self.x, self.y)
        playButton = self.menuItem("Play", self.play, self.x, self.y)
        print(playButton.width_range, playButton.height_range)
        self.add(playButton, z=1)

    def on_enter(self):
        super().on_enter()
        self.do(Delay(1) + FadeIn(2))

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
        global x, y
        self.add(titleLabel)
        titleLabel.do(AccelDeccel(MoveTo((x / 2, y * 0.9), 2)))
        self.add(mainMenu())


class loadingScreen(BaseWindow):
    is_event_handler = True

    def __init__(self):
        super(loadingScreen, self).__init__()
        x, y = cocos.director.director.get_window_size()
        titleLabel.position = x / 2, y * 0.7
        self.add(titleLabel)
        titleLabel.do(FadeIn(1))

    def on_enter(self):
        super().on_enter()
        game_loading()

if __name__=="__main__":
    print("This file cannot be run directly, please run main.py to start the game.")