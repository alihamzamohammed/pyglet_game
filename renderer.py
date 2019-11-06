import cocos
from cocos.text import Label
from cocos import scene
from cocos.layer import Layer
from cocos.director import director


class rendererWindow(Layer):

    def __init__(self):
        super(rendererWindow, self).__init__()

director.init(height=1280, height=720, caption="Game", fullscreen=True)
director.run(scene.Scene(rendererWindow()))