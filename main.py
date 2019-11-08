import sys, os
import cocos
from cocos.director import director
from cocos import scene
import renderer

class loadingScreen(renderer.BaseWindow):
    def __init__(self):
        super(loadingScreen, self).__init__()


def main():
    director.init(width=1280, height=720, caption="Game", fullscreen=False)
    director.run(scene.Scene(loadingScreen()))
    

if __name__=="__main__":
    main()  