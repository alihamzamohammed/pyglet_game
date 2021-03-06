import cocos
import pyglet
import xml.etree.ElementTree as et
import logger
import os

class ItemPack():
    
    modeType = "itempack"
    
    def __init__(self, folder, idx):
        super().__init__()
        self.folder = folder
        self.idx = idx
        if not os.path.exists(self.folder):
            raise ItemPackCorrupt("Folder not found! Item pack will not be loaded!")
        if "main.xml" in os.listdir(self.folder):
            self.main = os.path.join(self.folder, "main.xml")
        else:
            raise ItemPackCorrupt("main.xml not found in item pack " + self.folder + ", item pack will not be loaded!")
        try:
            self._itm = et.parse(self.main)
        except et.ParseError:
            raise ItemPackCorrupt("main.xml in item pack " + self.folder + " is corrupt, item pack will not be loaded!")
        self.tags = {}
        self.items = []
        self.item_xml = {}
        self.item_data = {}
        self.item_res = {}

        for item in list(self._itm.getroot()):
            
            if item.tag == "name":
                self.name = item.text
            
            if item.tag == "desc" or item.tag == "description":
                self.desc = item.text
            
            if not hasattr(self, "required"):
                self.required = {}
            if item.tag == "required":
                for a in item.attrib:
                    if not item.attrib[a] in self.required:
                        self.required[item.attrib[a]] = []
                    self.required[item.attrib[a]].append(item.text)
            
            for listreq in self.required:
                for req in range(len(self.required[listreq])):
                    if not os.path.isfile(os.getcwd() + "\\" + self.folder + "\\" + self.required[listreq][req]):
                        print(os.getcwd() + "\\" + self.folder + "\\" + self.required[listreq][req])
                        raise DependencyNotFound("File " + self.required[listreq][req] + " is not found, item pack " + self.folder + " will not be loaded!")
            
            if item.tag == "item" and item.text not in self.items:
                self.item_xml[item.text[:-4]] = item.text
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
        else:
            for itempath in self.items:
                res = cocos.tiles.load_tiles(self.folder + "\\" + itempath)
                self.item_res[itempath[:-4]] = res
                self.item_data[itempath[:-4]] = res.contents[None][itempath[:-4]]        

        # ~ Is this needed?
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
    global itempacks, folder
    itempacks = {}
    folder = "//items//"
    for itmfolder in [f.name for f in os.scandir(os.getcwd() + folder) if f.is_dir()]:
        if itmfolder != "__pycache__":
            try:
                itempacks[itmfolder] = ItemPack(folder[2:] + itmfolder, itmfolder)
            except ItemPackCorrupt as e:
                logger.addLog(e.message, logger.loglevel["warning"])
            except DependencyNotFound as e:
                logger.addLog(e.message, logger.loglevel["warning"])