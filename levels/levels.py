import cocos
import pyglet
import xml.etree.ElementTree as et
import os
import cfg

class Level():

    def __init__(self, folder):
        super().__init__()
        self.folder = folder
        if not os.path.exists(self.folder):
            raise LevelCorrupt
        if "main.xml" in os.listdir(self.folder):
            self.main = os.path.join(self.folder, "main.xml")
        else:
            raise None
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

    def __repr__(self):
        return self.data

    def __str__(self):
        return self.name

class LevelCorrupt(Exception):
    pass

class DependencyNotFound(Exception):
    pass


def levelLoad(lvlstr):
    load = Level(lvlstr)
    cfg.loadedLevel = load
    return load