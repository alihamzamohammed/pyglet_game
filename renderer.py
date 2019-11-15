import cocos
from cocos.text import Label
from cocos import scene
from cocos import layer
from cocos.actions import *
from cocos.director import director
import resources
import time

class BaseWindow(scene.Scene):

    def __init__(self):
        super(BaseWindow, self).__init__()

class loadingScreen(BaseWindow):

    def __init__(self):
        super(loadingScreen, self).__init__()
        loadingTitle = cocos.text.Label(
            "Game Title",
            font_name=resources.font[1],
            font_size=32,
            anchor_y="top",
            anchor_x="center"
        )
        x, y = cocos.director.director.get_window_size()
        loadingTitle.position = x / 2, y * 0.95
        self.add(loadingTitle)
        loadingTitle.do(FadeIn(1))

if __name__=="__main__":
    print("This file cannot be run directly, please run main.py to start the game.")
