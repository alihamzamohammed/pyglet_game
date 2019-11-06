import sys, os
import cocos
from cocos.director import director
import renderer

def main():
    director.init(width=1280, height=720, caption="Game", fullscreen=False)
    director.run(scene.Scene(rendererWindow()))

if __name__=="__main__":
    main()  