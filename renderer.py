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
import resources
import random
import time

x, y = director.window.width, director.window.height
reswidth, resheight = [int(res) for res in cfg.configuration["Core"]["defaultres"].split("x")]

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
    
    def __init__(self, label, eventName, buttonorder = 1, call = False):
        super().__init__()
        global x, y
        #x, y = director.get_virtual_coordinates(x, y)
        self.call = call
        self.buttonorder = buttonorder
        self.eventName = eventName
        self.label = label
        self.bgImage = Sprite("menuButton.png") # Replace with resource pack image
        self.lbl = Label(self.label, anchor_x="center", anchor_y="center")
        
        self.x = x / 2
        self.TOPBTNPOS = 0.68
        self.y = y * (self.TOPBTNPOS - (0.16 * (self.buttonorder - 1)))
                
        self.width = self.bgImage.width
        self.height = self.bgImage.height
        
        self.add(self.bgImage, z = 0)
        self.add(self.lbl, z = 1)
        
        self.width_range = [int(self.x - (self.bgImage.width / 2)), int(self.x + (self.bgImage.width / 2))]
        self.height_range = [int(self.y - (self.bgImage.height / 2)), int(self.y + (self.bgImage.height / 2))]
        
        self.animate()

        self.schedule_interval(self.setWH, 1)
        self.resume_scheduler()

    def setWH(self, dt):
        x, y = director.window.width, director.window.height
        scalex = x / reswidth
        scaley = y / resheight
        self.width_range = [int((x / 2) - ((self.bgImage.width * scalex) / 2)), int((x / 2) + ((self.bgImage.width * scalex) / 2))]
        self.height_range = [int((y * (self.TOPBTNPOS - (0.16 * (self.buttonorder - 1)))) - ((self.bgImage.height * scaley) / 2)), int((y * (self.TOPBTNPOS - (0.16 * (self.buttonorder - 1)))) + ((self.bgImage.height * scaley) / 2))]

    def on_mouse_motion(self, x, y, dx, dy):
        if x in range(self.width_range[0], self.width_range[1]) and y in range(self.height_range[0], self.height_range[1]):
            self.bgImage.image = pyglet.resource.image("menuButtonHovered.png")
        else:
            self.bgImage.image = pyglet.resource.image("menuButton.png")

    def on_mouse_press(self, x, y, buttons, modifiers):
        if x in range(self.width_range[0], self.width_range[1]) and y in range(self.height_range[0], self.height_range[1]):
            self.eventName()
            self.bgImage.image = pyglet.resource.image("menuButtonClicked.png")
            self.lbl.element.color = (0, 0, 0, 255)

    def animate(self):
        mvx = self.x
        mvy = self.y
        # ODD
        if not self.buttonorder % 2 == 0:
            self.x = -self.width
            self.do(Delay(0.7) + AccelDeccel(MoveTo((mvx, mvy), 1.5)))
        # EVEN
        else:
            self.x = x + self.width
            self.do(Delay(0.7) + AccelDeccel(MoveTo((mvx, mvy), 1.5)))

class sectionButtons(layer.Layer): 

    

    def __init__(self):
        super().__init__()

    
'''Game scenes'''
class BaseWindow(scene.Scene):
    def __init__(self):
        super(BaseWindow, self).__init__()

class SettingsScreen(BaseWindow):

    def __init__(self):
        super().__init__() 
        self.settingsLabel = cocos.text.Label(
            "Settings",
            font_name=resources.font[1],
            font_size=50,
            anchor_y="center",
            anchor_x="center"
        )
        self.settingsLabel.position = x / 2, y * 0.9
        
        test = Test()
        test.x = 100
        test.y = 100
        test.width = 1000
        test.height = 1000
        self.add(test)

        self.add(self.settingsLabel)

    def on_enter(self):
        super().on_enter()
    
    def on_mouse_motion(self, x, y, dx, dy):
        print("Moving")

    def on_mouse_press(self, x, y, buttons, modifiers):
        events.rendererevents.dispatch_event("test")

class Test(layer.Layer):

    is_event_handler = True

    def __init__(self):
        super().__init__()

    def on_mouse_press(self, x, y, buttons, modifiers):
        events.rendererevents.test()

class MainMenuScreen(BaseWindow):
    is_event_handler = True

    def __init__(self):
        super(MainMenuScreen, self).__init__()
        global x, y
        self.add(titleLabel)
        titleLabel.do(AccelDeccel(MoveTo((x / 2, y * 0.9), 1.5)))
        
        playButton = menuItem("Play Game", events.rendererevents.onPlayButtonClick, 1)
        multiplayerButton = menuItem("Multiplayer", events.rendererevents.onMultiplayerButtonClick, 2)
        settingsButton = menuItem("Settings", events.rendererevents.onSettingsButtonClick, 3)
        quitButton = menuItem("Quit Game", events.rendererevents.onQuitButtonClicked, 4)

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