import cocos
from cocos.text import Label
from cocos import scene
from cocos.layer import Layer
from cocos.director import director
import main

class BaseWindow(Layer):

    def __init__(self):
        super(BaseWindow, self).__init__()

class loadingScreen(BaseWindow):
    def __init__(self):
        super(loadingScreen, self).__init__()
        title = cocos.text.Label(
            "Game Title",
            font_name=main.font,
            font_size=32
        )
        title.position = 100, 100
        self.add(title)


if __name__=="__main__":
    print("This file cannot be run directly, please run main.py to start the game.")
