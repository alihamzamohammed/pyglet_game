import cocos
from cocos.text import Label
from cocos import scene
from cocos.layer import Layer
from cocos.director import director


class rendererWindow(Layer):

    def __init__(self):
        super(rendererWindow, self).__init__()

director.init(width=1280, height=720, caption="Game", fullscreen=False)
director.run(scene.Scene(rendererWindow()))

#if __name__=="__main__":
 #   print("This file cannot be run directly, please run main.py to start the game.")