import cocos
import pyglet
import xml.etree.ElementTree as et
import os
import cfg
import logger

class Level():

    def __init__(self, folder, idx):
        super().__init__()
        self.folder = folder
        self.idx = idx
        if not os.path.exists(self.folder):
            raise LevelCorrupt("Folder not found! Level will not be loaded!")
        if "main.xml" in os.listdir(self.folder):
            self.main = os.path.join(self.folder, "main.xml")
        else:
            raise LevelCorrupt("main.xml not found in Level " + self.folder + ", level will not be loaded!")
        self._lvl = et.parse(self.main)
        self.tags = {}
        for item in list(self._lvl.getroot()):
            if item.tag == "name" and item.text != None:
                self.name = item.text
            if (item.tag == "desc" or item.tag == "description") and item.text != None:
                self.desc = item.text
            if item.tag == "data" and item.text != None:
                if os.path.isfile(os.path.join(self.folder, item.text)):
                    self.datapath = os.path.join(self.folder, item.text)
                    self.data = et.parse(self.datapath)
                else:
                    raise DependencyNotFound(item.text + " is listed as a dependency of " + self.folder + " but was not found, level will not be loaded!")
            if item.tag == "background" and item.text != None:
                if "png" in item.text or "jpg" in item.text:
                    pyglet.resource.path.append(os.getcwd() + "\\" + self.folder)
                    pyglet.resource.reindex()
                    self.background = item.text
                elif any(char.isdigit() for char in item.text) and "," in item.text:
                    self.background = tuple(item.text)
            if item.tag == "thumbnail" and item.text != None:
                self.thumbnail = item.text
            self.tags[item.tag] = item.text
            self.tags.update(self._lvl.getroot().attrib)
        if not hasattr(self, "name"):
            self.name = "Level"
        if not hasattr(self, "desc"):
            self.desc = "No description"
        if not hasattr(self, "data"):
            raise LevelCorrupt("Level " + self.folder + " has no content, level will not be loaded!")
        if not hasattr(self, "background"):
            self.background = (100, 120, 150, 255)            
        if not hasattr(self, "thumbnail"):
            self.thumbnail = "defaultThumbnail.png"

    #def __str__(self):
     #   return self.name

class LevelCorrupt(Exception):

    def __init__(self, message, *args, **kwargs):
        self.message = message
        

class DependencyNotFound(Exception):
    
    def __init__(self, message, *args, **kwargs):
        self.message = message

def levelLoad(lvlstr):
    load = levels[lvlstr]
    cfg.loadedLevel = load
    return load

def init():
    global levels
    levels = {}
    folder = "//levels//"
    for lvlfolder in [f.name for f in os.scandir(os.getcwd() + folder) if f.is_dir()]:
        if lvlfolder != "__pycache__":
            try:
                levels[lvlfolder] = Level(folder[2:] + lvlfolder, lvlfolder)
            except LevelCorrupt as e:
                logger.addLog(e.message, logger.loglevel["warning"])
            except DependencyNotFound as e:
                logger.addLog(e.message, logger.loglevel["warning"])