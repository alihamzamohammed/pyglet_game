import pyglet
import cocos
from cocos import tiles, text, sprite, layer, scene, batch
from cocos.director import director
import xml.etree.ElementTree as et
import levels
import items
import logger
import cfg

reswidth, resheight = [int(res) for res in cfg.resolution.split("x")]


class LevelNotFound(Exception):
    
    def __init__(self, message = "The level was not found in the game's loaded levels.", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = message

class GridCellSprite(layer.Layer):

    is_event_handler = True

    def __init__(self):
        super().__init__()
        self.bgImage = sprite.Sprite()
        self.add(self.bgImage)

    def on_mouse_motion(self, x, y, dx, dy):
        print("hello")
        #if self.contains(x, y):
         #   self.image = pyglet.resource.image("leveleditorItemHovered.png")
          #  print(x, y)


class LevelEditor(scene.Scene):

    is_event_handler = True

    def __init__(self, level):
        super().__init__()
        if not isinstance(level, levels.Level):
            raise LevelNotFound
        self.level = level
        self.levelData = tiles.load(self.level.datapath)
        self.tilemap_decorations = self.levelData["decorations"]
        self.tilemap_walls = self.levelData["walls"]
        
        self.gridLayer = layer.ScrollableLayer()
        self.gridList = []
        self.gridBatch = batch.BatchNode()
        self.gridLayer.add(self.gridBatch)
        ## ! Impelentation Inefficient
        #column, cell = 0
        #for column in self.tilemap_walls.cells:
        #    self.gridList.append([])
        #    for cell in column:
        #        gridCell = GridCellSprite("leveleditorItemClicked.png")
        #        gridCell.x = ((cell.i + 1) * 32) - 16
        #        gridCell.y = ((cell.j + 1) * 32) - 16
        #        gridCell.opacity = 100
        #        self.gridBatch.add(gridCell)
        #        self.gridList[cell.i].append(gridCell)
           #   cell +=1
            #column += 1

        self.scroller = layer.ScrollingManager()
        self.scroller.scale = 0.8
        self.scroller.x = 0
        self.scroller.y = 0
        self.scroller.add(self.tilemap_decorations, z=-1)
        self.scroller.add(self.tilemap_walls, z=0)
        self.scroller.add(self.gridLayer, z=2)

        self.add(self.scroller)

    def on_mouse_motion(self, x, y, dx, dy):
        self.gridList[(x // 32) - 1][(y // 32) - 1].image(pyglet.resource.image("leveleditorItemHovered.png"))
        print((x//32)-1, (y//32)-1)

# * cocos.tiles.load has a function names save_xml(), which saves the loaded folder to xml
# * Along with the ability to change the shown tile directly on the layer and have it reflect in the game, this can be used for level editor
# * items.itempacks now has loaded resource and tile objects for each item in an item pack. This can be used to directly change data in the tileset.
# * However, care must be taken to find if the item is not in the level's required, that is it added there, otherwise the level will not work at all
# * This can be done by finding the res class in the item pack's item_res dictionary, and adding it to the level's required list as a tuple
# * This check can be done when an item is changed on the level 

# ! Cocos level renderer can be refreshed by set_dirty()