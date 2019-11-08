import sys, os
import cocos
from cocos.director import director
from cocos import scene
import renderer
import configparser

defaultconfigfile = "settings.ini"
config = {}
font = ""

def configread(configFile):
    temp = {}
    conf = configparser.ConfigParser()
    conf.read(configFile)
    for section in conf.sections():
        for option in conf.options(section):
            temp[option] = conf.get(section, option)
        config[section] = temp
        temp = {}

def resourceLoad():
    respack = config["Core"]["defaultresource"]
    global font
    font = "resource/" + respack + "/fonts/default.ttf"
    cocos.pyglet.font.add_file(font)

def main():
    director.init(width=1280, height=720, caption="Game", fullscreen=False)
    director.run(scene.Scene(renderer.loadingScreen()))

if __name__=="__main__":
    configread(defaultconfigfile)
    resourceLoad()
    print(font)
    main()  