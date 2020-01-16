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
        x, y = cocos.director.director.get_window_size()

        menuitems = []

        menuitems.append( MenuItem("Play", self.play) )
        menuitems.append( MenuItem("Multiplayer", self.multiplayer) )
        menuitems.append( MenuItem("Settings", self.settings) )
        menuitems.append( MenuItem("Quit Game", self.quit) )

        self.create_menu(menuitems)
        
    #def on_enter(self):
     #   super().on_enter()
      #  self.do(Delay(2) + FadeIn(10))
    
    # class menuItem(MenuItem):

    #     def __init__(self, label, callback_func, *args, **kwargs):
    #         super().__init__(label, callback_func, *args, **kwargs)
        
    #     def generateWidgets(self, pos_x, pos_y, font_item, font_item_selected):
    #         super().generateWidgets(pos_x, pos_y, font_item, font_item_selected)
    #         self.item = self.ImageLabel(self.label)
    #         self.item_selected = self.ImageLabel(self.label)

    #     class ImageLabel(layer.Layer):

    #         def __init__(self, label):
    #             super().__init__()
    #             lbl = Label(label)
    #             #self.add(lbl, z=1)
    #             sprt = Sprite("image.png")
    #             self.add(sprt, z=0)
    #             self.content_width = sprt.width
    #             self.content_height = sprt.height

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


class MainMenuLayer(layer.Layer):

    def __init__(self):
        super().__init__()
            #mainmenu = MainMenu()
            #self.add(MainMenu())

    def on_enter(self):
        super().on_enter()
        self.add(MainMenu(), z=1)
        self.do(Delay(2) + FadeIn(1))


class MainMenuScreen(BaseWindow):
    is_event_handler = True

    def __init__(self):
        super(MainMenuScreen, self).__init__()
        x, y = cocos.director.director.get_window_size()
        self.add(titleLabel)
        titleLabel.do(AccelDeccel(MoveTo((x / 2, y * 0.85), 2)))
        mainmenulayer = MainMenuLayer()
        self.add(mainmenulayer)


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