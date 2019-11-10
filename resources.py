import main
import cocos
from cocos import text
from fontTools import ttLib
import logging
from logging import addLog

resourcePack = "default" 
font = ""

FONT_SPECIFIER_NAME_ID = 4
FONT_SPECIFIER_FAMILY_ID = 1
def shortName(font):
    """Get the short name from the font's names table"""
    name = ""
    family = ""
    for record in font['name'].names:
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
    if not main.config == {}:
        resourcePack = main.config["Core"]["defaultresource"]
    else:
        resourcePack = "default"
        addLog("No specified resource pack, using default!", logging.loglevel["warning"])

def fontLoad():
    if not resourcePack == "":
        fontpath = "resources\\" + resourcePack + "\\fonts\\default.ttf"
        cocos.text.pyglet.font.add_file(fontpath)
        tt = ttLib.TTFont(fontpath)
        global font
        font = shortName(tt)
    else:
        print("Resource pack error!")

def resourceLoad():
    """Loads all resources from the set resource pack"""
    getResourcePack()
    fontLoad()
    