import cocos
from cocos.text import Label
from cocos import scene
from cocos.layer import Layer
from cocos.director import director
import resources

class BaseWindow(Layer):

    def __init__(self):
        super(BaseWindow, self).__init__()

class loadingScreen(BaseWindow):
    def __init__(self):
        super(loadingScreen, self).__init__()
        title = cocos.text.Label(
            "Game Title",
            font_name=resources.font[1],
            font_size=32,
            anchor_y="top",
            anchor_x="center"
        )
        x, y = cocos.director.director.get_window_size()
        title.position = x / 2, y * 0.95
        self.add(title)


if __name__=="__main__":
    print("This file cannot be run directly, please run main.py to start the game.")
