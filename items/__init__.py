import cocos
import pyglet
import xml.etree.ElementTree as et
import logger
import os

class ItemPack():

    def __init__(self, folder):
        super().__init__()
        self.folder = folder
        if not os.path.exists(self.folder):
            raise ItemPackCorrupt("Folder not found! Item pack will not be loaded!")
        if "main.xml" in os.listdir(self.folder):
            self.main = os.path.join(self.folder, "main.xml")
        else:
            raise ItemPackCorrupt("main.xml not found in item pack " + self.folder + ", item pack will not be loaded!")
        self._itm = et.parse(self.main)
        self.tags = {}
        self.items = []
        for item in list(self._itm.getroot()):
            
            if item.tag == "name":
                self.name = item.text
            
            if item.tag == "desc" or item.tag == "description":
                self.desc = item.text
            
            self.required = {}
            if item.tag == "required":
                for a in item.attrib:
                    self.required[item.attrib[a]] = item.text
            
            for req in self.required:
                if not os.path.isfile(os.getcwd() + "\\" + self.folder + "\\" + self.required[req]):
                    raise DependencyNotFound("File " + self.required[req] + " is not found, item pack " + self.folder + " will not be loaded!")
            
            if item.tag == "item" and item.text not in self.items:
                self.items.append(item.text)
            
            if item.tag == "thumbnail":
                pyglet.resource.path.append(os.getcwd() + "\\" + self.folder)
                pyglet.resource.reindex()
                self.thumbnail = item.text
            self.tags[item.tag] = item.text
            self.tags.update(self._itm.getroot().attrib)
        
        if not hasattr(self, "name"):
            self.name = "Item Pack"
        
        if not hasattr(self, "desc"):
            self.desc = "No description"
        
        if self.items == []:
            logger.addLog("Item pack " + self.name + " at path " + self.folder + " has no declared items.", logger.loglevel["info"])
        
        if not hasattr(self, "background"):
            self.background = (100, 120, 150, 255)

    def __str__(self):
        return self.name

class ItemPackCorrupt(Exception):
    
    def __init__(self, message, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = message

class DependencyNotFound(Exception):

    def __init__(self, message, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = message

# ?: Custom code delcared here for specific items that instantiate a class, such as trampoline needs to override existing code from the game mode to implement new functionality.
# ?: One way in which this could be done is through decorators, but this will need thorough research in order to implement properly.

def init():
    global itempacks
    itempacks = {}
    folder = "//items//"
    for itmfolder in [f.name for f in os.scandir(os.getcwd() + folder) if f.is_dir()]:
        if itmfolder != "__pycache__":
            try:
                itempacks[itmfolder] = ItemPack(folder[2:] + itmfolder)
            except ItemPackCorrupt as e:
                logger.addLog(e.message, logger.loglevel["warning"])
            except DependencyNotFound as e:
                logger.addLog(e.message, logger.loglevel["warning"])