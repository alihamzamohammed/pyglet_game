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
            raise LevelCorrupt("Folder not found! Level will not be loaded!")
            return None
        if "main.xml" in os.listdir(self.folder):
            self.main = os.path.join(self.folder, "main.xml")
        else:
            raise LevelCorrupt("main.xml not found in Level " + self.folder + ", level will not be loaded!")
            return None
        self._lvl = et.parse(self.main)
        self.tags = {}
        for item in list(self._lvl.getroot()):
            if item.tag == "name":
                self.name = item.text
            elif item.tag == "desc" or item.tag == "description":
                self.desc = item.text
            elif item.tag == "data":
                if os.path.isfile(os.path.join(self.folder, item.text)):
                    self.datapath = os.path.join(self.folder, item.text)
                    self.data = et.parse(self.datapath)
                else:
                    raise LevelCorrupt(item.text + " is listed as a dependency of " + self.folder + " but was not found, level will not be loaded!")
                    return None
            elif item.tag == "background":
                self.background = item.text
            else:
                self.tags[item.tag] = item.text
            self.tags.update(self._lvl.getroot().attrib)

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
    for lvlfolder in [f.name for f in os.scandir(os.getcwd() + folder) if f.is_dir()]:
        if lvlfolder is not "__pycache__":
            try:
                levels[lvlfolder] = Level(folder[2:] + lvlfolder)
            except LevelCorrupt as e:
                logger.addLog(e.message, logger.loglevel["warning"])