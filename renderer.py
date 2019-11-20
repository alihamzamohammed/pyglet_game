import cocos
from cocos.text import Label
from cocos import scene
from cocos import layer
from cocos.actions import *
from cocos.director import director
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

class BaseWindow(scene.Scene):

    def __init__(self):
        super(BaseWindow, self).__init__()

class loadingScreen(BaseWindow):

    def __init__(self):
        super(loadingScreen, self).__init__()
        x, y = cocos.director.director.get_window_size()
        title.position = x / 2, y * 0.72
        self.add(title)
        title.do(FadeIn(1))

if __name__=="__main__":
    print("This file cannot be run directly, please run main.py to start the game.")