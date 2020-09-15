import os
import cfg
import cocos
import pickle
from cocos import text
from fontTools import ttLib
import pyglet
from cocos.actions import *
import logger
resourcePack = "default"
font = ""
animations = {}
path = os.getcwd()

FONT_SPECIFIER_NAME_ID = 4
FONT_SPECIFIER_FAMILY_ID = 1
def shortName(font):
    """Get the short name from the font's names table"""
    name = ""
    family = ""
    for record in font["name"].names:
        if b'\x00' in record.string:
            name_str = record.string.decode('utf-16-be')
        else:   
            name_str = record.string.decode('utf-8')
        if record.nameID == FONT_SPECIFIER_NAME_ID and not name:
            name = name_str
        elif record.nameID == FONT_SPECIFIER_FAMILY_ID and not family: 
            family = name_str
        if name and family: break
    return [name, family]

def getResourcePack():
    global resourcePack
    if not cfg.configuration == {}:
        resourcePack = cfg.configuration["Core"]["defaultresource"]
    else:
        resourcePack = "default"
        logger.addLog("No specified resource pack, using default!", logger.loglevel["warning"])

def fontLoad():
    global resourcePack
    global path
    if not resourcePack == "":
        fontpath = path + "\\resources\\" + resourcePack + "\\fonts\\default.ttf"
        pyglet.font.add_file(fontpath)
        tt = ttLib.TTFont(fontpath)
        global font
        font = shortName(tt)
    else:
        logger.addLog("Resource pack not found!", logger.loglevel["warning"])
        # Switch to default resource pack

def animLoad():
    global resourcePack
    global path
    if not resourcePack == "":
        animpath = path + "\\resources\\" + resourcePack + "\\animations\\animations.anim"
        try:
            with open(animpath, "rb") as file:
                global animations
                #animations = pickle.load(file)
        except pickle.PickleError:
            logger.addLog("Animation file not decodable", logger.loglevel["warning"])
        except FileNotFoundError:
            logger.addLog("Animation file not found!", logger.loglevel["warning"])
            # Switch to default resource pack
    else:
        logger.addLog("Resource pack not found!", logger.loglevel["warning"])

def resourceLoad():
    """Loads all resources from the set resource pack"""
    getResourcePack()
    fontLoad()
    animLoad()
    #if pyglet.resource.path is []:
    pyglet.resource.path = [path + "\\resources\\" + resourcePack, path + "\\resources\\" + resourcePack + "\\images"]
    # TODO: Add code to check if resource pack is being switched or initialisation of resource pack. Maybe through another function, with new resource pack as argument?
    # TODO: Will need to be tested on 2 resource packs, and switching mechanism in-game.
    pyglet.resource.reindex()