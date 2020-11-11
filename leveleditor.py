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

class LevelGridLayer(layer.ScrollableLayer):

    is_event_handler = True

    def __init__(self, parallax=1, **kwargs):
        super().__init__(parallax=parallax)
        self.gridList = []
        self.gridBatch = batch.BatchNode()
        self.scroller = kwargs["scroller"]
        self.level = kwargs["level"]
        self.walls = kwargs["walls"]
        self.decorations = kwargs["decorations"]
        self.hovered = None
        self.selected = []
        for column in kwargs["walls"].cells:
            self.gridList.append([])
            for cell in column:
                gridCell = sprite.Sprite("leveleditorItem.png")
                gridCell.x = ((cell.i + 1) * 32) - 16
                gridCell.y = ((cell.j + 1) * 32) - 16
                self.gridBatch.add(gridCell)
                self.gridList[cell.i].append([gridCell, False])
        self.add(self.gridBatch)

    def on_mouse_motion(self, x, y, dx, dy):
        x, y = self.scroller.screen_to_world(x, y)
        try:
            cell = self.gridList[x // 32][y // 32]
            if self.hovered is not None:
                if self.hovered[1]:
                    self.hovered[0].image = pyglet.resource.image("leveleditorItemClicked.png")
                else:
                    self.hovered[0].image = pyglet.resource.image("leveleditorItem.png")
            cell[0].image = pyglet.resource.image("leveleditorItemHovered.png")
            self.hovered = cell
        except IndexError:
            pass

    def on_mouse_press(self, x, y, buttons, modifiers):
        x, y = self.scroller.screen_to_world(x, y)
        try:
            if self.hovered[1]:
                self.hovered[0].image = pyglet.resource.image("leveleditorItem.png")
                self.hovered[1] = False
            else:
                self.hovered[0].image = pyglet.resource.image("leveleditorItemClicked.png")
                self.hovered[1] = True
        except IndexError:
            pass

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
        if isinstance(self.level.background, str):
            self.bgLayer = layer.ScrollableLayer()
            self.bgLayer.parallax = 0.5
            bgImage = cocos.sprite.Sprite(self.level.background)
            # TODO: Add code to scale image to viewport, then tile it
            self.bgLayer.add(bgImage)

        self.scroller = layer.ScrollingManager()
        
        self.scroller.scale = 0.8
        self.scroller.x = 0
        self.scroller.y = 0
        self.scroller.set_focus(800, 0)
        self.scroller.add(self.tilemap_decorations, z=-1)
        self.scroller.add(self.tilemap_walls, z=0)
        self.gridLayer = LevelGridLayer(walls=self.tilemap_walls, decorations=self.tilemap_decorations, scroller=self.scroller, level=self.level)#layer.ScrollableLayer()
        self.scroller.add(self.gridLayer, z=2)
        self.scroller.add(self.bgLayer, z=-5)

        self.add(self.scroller)

# * cocos.tiles.load has a function names save_xml(), which saves the loaded folder to xml
# * Along with the ability to change the shown tile directly on the layer and have it reflect in the game, this can be used for level editor
# * items.itempacks now has loaded resource and tile objects for each item in an item pack. This can be used to directly change data in the tileset.
# * However, care must be taken to find if the item is not in the level's required, that is it added there, otherwise the level will not work at all
# * This can be done by finding the res class in the item pack's item_res dictionary, and adding it to the level's required list as a tuple
# * This check can be done when an item is changed on the level 

# ! Cocos level renderer can be refreshed by set_dirty()
# ! This should only be done when cells have been changed, because it causes a performance hit