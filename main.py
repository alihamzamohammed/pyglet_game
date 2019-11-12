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
    director.init(width=int(cfg.configuration["Core"]["defaultres"].split("x")[0]), height=int(cfg.configuration["Core"]["defaultres"].split("x")[1]), caption="Game", fullscreen=False)
    #bool(cfg.configuration["Core"]["fullscreen"])
    director.run(scene.Scene(renderer.loadingScreen()))

if __name__=="__main__":
    cfg.init()
    defaultconfigfile = "settings.ini"
    configread(defaultconfigfile)
    resources.resourceLoad()
    logger.init()
    print(cfg.configuration["Core"]["fullscreen"])
    logger.addLog("Starting game.", logger.loglevel["info"])
    main()

