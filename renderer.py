import cocos
from cocos.text import Label
from cocos import scene
from cocos.layer import Layer
from cocos.director import director


class BaseWindow(Layer):

    def __init__(self):
        super(BaseWindow, self).__init__()


if __name__=="__main__":
    print("This file cannot be run directly, please run main.py to start the game.")

