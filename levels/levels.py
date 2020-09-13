import cocos
import pyglet
import xml.etree.ElementTree as et
import os
import cfg
import logger

class Level():

    def __init__(self, folder):
        super().__init__()
        self.folder = folder
        if not os.path.exists(self.folder):
            raise LevelCorrupt("Folder not found! Level not loaded!")
        if "main.xml" in os.listdir(self.folder):
            self.main = os.path.join(self.folder, "main.xml")
        else:
            raise LevelCorrupt("main.xml not found in Level " + self.folder + ", level will not be loaded!")
        self._lvl = et.parse(self.main)
        self.tags = {}
        for item in list(self._lvl.getroot()):
            if item.tag == "name":
                self.name = item.text
            elif item.tag == "desc" or item.tag == "description":
                self.desc = item.text
            elif item.tag == "data":
                self.datapath = os.path.join(self.folder, item.text)
                self.data = et.parse(self.datapath)
            elif item.tag == "background":
                self.background = item.text
            else:
                self.tags[item.tag] = item.text
            self.tags.update(self._lvl.getroot().attrib)

    #def __repr__(self):
     #   return self.data

    def __str__(self):
        return self.name

class LevelCorrupt(Exception):

    def __init__(self, message, *args, **kwargs):
        self.message = message
        

class DependencyNotFound(Exception):
    pass

def levelLoad(lvlstr):
    load = levels[lvlstr]
    cfg.loadedLevel = load
    return load

def init():
    global levels
    levels = {}
    folder = "//levels//"
    for lvlfolder in [x[1] for x in os.walk(os.getcwd() + folder)]:
        if lvlfolder is not []:
            for lvl in lvlfolder:
                if lvl is not "" or not "__pycache__":
                    try:
                        levels[lvl] = Level(folder[2:] + lvl)
                    except LevelCorrupt as e:
                        logger.addLog(e.message, logger.loglevel["warning"])
    #print(str(levels))
