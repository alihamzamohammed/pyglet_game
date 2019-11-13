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
    reswidth = int(cfg.configuration["Core"]["defaultres"].split("x")[0])
    resheight = int(cfg.configuration["Core"]["defaultres"].split("x")[1])
    fullscreen = True if cfg.configuration["Core"]["fullscreen"] == "True" else False
    logger.addLog("Resolution is " + str(reswidth) + "x" + str(resheight), logger.loglevel["info"])
    if fullscreen == True:
        logger.addLog("Fullscreen is enabled", logger.loglevel["info"])
    else:
        logger.addLog("Fullscreen is disabled", logger.loglevel["info"])

    director.init(width=reswidth, height=resheight, caption="Game", fullscreen=fullscreen)
    director.run(renderer.loadingScreen())

if __name__=="__main__":
    cfg.init()
    defaultconfigfile = "settings.ini"
    configread(defaultconfigfile)
    resources.resourceLoad()
    logger.init()
    logger.addLog("Starting game.", logger.loglevel["info"])
    main()