import cfg
import sys, os
import cocos
from cocos.director import director
from cocos import scene
from cocos import text
import renderer
import configparser
import resources
import logger

def configread(configFile):
    temp = {}
    conf = configparser.ConfigParser()
    conf.read(configFile)
    for section in conf.sections():
        for option in conf.options(section):
            temp[option] = conf.get(section, option)
        cfg.configuration[section] = temp
        temp = {}

def main():
    director.init(width=1280, height=720, caption="Game", fullscreen=False)
    director.run(scene.Scene(renderer.loadingScreen()))

if __name__=="__main__":
    cfg.init()
    defaultconfigfile = "settings.ini"
    configread(defaultconfigfile)
    resources.resourceLoad()
    logger.init()
    logger.addLog("Starting game.", logger.loglevel["info"])
    main()
