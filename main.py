import sys, os
import cocos
from cocos.director import director
from cocos import scene
import renderer


def resourceLoad():
    pass

def main():
    director.init(width=1280, height=720, caption="Game", fullscreen=False)
    director.run(scene.Scene(renderer.loadingScreen()))
    
if __name__=="__main__":
    main()  