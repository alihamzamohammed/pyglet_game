import cocos
from cocos.text import Label
from cocos import scene
from cocos.layer import Layer
from cocos.director import director


class rendererWindow(Layer):

    def __init__(self):
        super(rendererWindow, self).__init__()

director.init()
director.run(scene.Scene(rendererWindow()))