import sys, os, configparser
import cocos
from cocos.director import director

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
    logger.addLog("Resolution is " + str(reswidth) + "x" + str(resheight), logger.loglevel["info"])
    if fullscreen == True:
        logger.addLog("Fullscreen is enabled", logger.loglevel["info"])
    else:
        logger.addLog("Fullscreen is disabled", logger.loglevel["info"])
    director.run(renderer.loadingScreen())

if __name__=="__main__":
    import cfg
    cfg.init()
    defaultconfigfile = "settings.ini"
    configread(defaultconfigfile)
    import logger
    logger.init()
    reswidth = int(cfg.configuration["Core"]["defaultres"].split("x")[0])
    resheight = int(cfg.configuration["Core"]["defaultres"].split("x")[1])
    fullscreen = True if cfg.configuration["Core"]["fullscreen"] == "True" else False
    director.init(width=reswidth, height=resheight, caption="Game", fullscreen=fullscreen, autoscale=True)
    import resources
    resources.resourceLoad()
    logger.addLog("Starting game.", logger.loglevel["info"])
    import renderer
    main()