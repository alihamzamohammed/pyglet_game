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

class menuItem(layer.Layer):
    
    is_event_handler = True
    
    def __init__(self, label, eventName, buttonorder = 1): #, posx, posy):#, buttonorder = 1):
        super().__init__()
        global x, y

        self.buttonorder = buttonorder
        self.eventName = eventName
        self.label = label
        bgImage = Sprite("image.png") # Replace with resource pack image
        self.lbl = Label(self.label, anchor_x="center", anchor_y="center")
        
        self.x = x / 2
        if buttonorder == 1:
            self.y = y * 0.68
        elif buttonorder == 2:
            self.y = y * 0.52
        elif buttonorder == 3:
            self.y = y * 0.36
        elif buttonorder == 4:
            self.y = y * 0.20        
        
        print(self.x, self.y)
        
        self.width = bgImage.width
        self.height = bgImage.height
        
        self.add(bgImage, z = 0)
        self.add(self.lbl, z = 1)
        
        print(bgImage.width, bgImage.height)
        
        self.width_range = [int(self.x - (bgImage.width / 2)), int(self.x + (bgImage.width / 2))]
        self.height_range = [int(self.y - (bgImage.height / 2)), int(self.y + (bgImage.height / 2))]
        
        print(self.width_range, self.height_range)

    def on_mouse_motion(self, x, y, dx, dy):
        if x in range(self.width_range[0], self.width_range[1]) and y in range(self.height_range[0], self.height_range[1]):
            self.lbl.element.text = "Hovered"
        else:
            self.lbl.element.text = self.label

    def on_mouse_press(self, x, y, buttons, modifiers):
        if x in range(self.width_range[0], self.width_range[1]) and y in range(self.height_range[0], self.height_range[1]):
            self.callbackfunc
            self.lbl.element.text = "clicked"

    def on_enter(self):
        super().on_enter()
        mvx = self.x
        mvy = self.y
        if not self.buttonorder % 2 == 0:
            self.x = -self.width
            self.do(Delay(1) + AccelDeccel(MoveTo((mvx, mvy), 1.5)))
        else:
            self.x = x + self.width
            self.do(Delay(1) + AccelDeccel(MoveTo((mvx, mvy), 1.5)))

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
        
        playButton = menuItem("Play Game", "", 1)
        multiplayerButton = menuItem("Multiplayer", self.multiplayer, 2)
        settingsButton = menuItem("Settings", self.settings, 3)
        quitButton = menuItem("Quit Game", self.quit, 4)

        self.add(playButton)
        self.add(multiplayerButton)
        self.add(settingsButton)
        self.add(quitButton)

    def play(self):
        print("Play button pressed!")
    
    def multiplayer(self):
        pass
    
    def settings(self):
        pass

    def quit(self):
        pass

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