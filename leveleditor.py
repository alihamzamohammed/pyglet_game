import pyglet
import cocos
from cocos import tiles, text, sprite, layer, scene, batch
from cocos.director import director
import xml.etree.ElementTree as et
import levels
import items
import logger
import cfg
import resources
import elements
import events

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
        self.dragging = []
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
            cell[0].image = pyglet.resource.image("leveleditorItemActiveHovered.png" if cell[1] else "leveleditorItemHovered.png")
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

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        x, y = self.scroller.screen_to_world(x, y)
        try:
            if not self.gridList[x // 32][y // 32] in self.dragging:
                if self.gridList[x // 32][y // 32][1]:
                    self.gridList[x // 32][y // 32][0].image = pyglet.resource.image("leveleditorItem.png")
                    self.gridList[x // 32][y // 32][1] = False
                    self.dragging.append(self.gridList[x // 32][y // 32])
                else:
                    self.gridList[x // 32][y // 32][0].image = pyglet.resource.image("leveleditorItemClicked.png")
                    self.gridList[x // 32][y // 32][1] = True                    
                    self.dragging.append(self.gridList[x // 32][y // 32])
        except IndexError:
            pass

    def on_mouse_release(self, x, y, buttons, modifiers):
        self.dragging = []

class LevelEditor(scene.Scene):

    is_event_handler = True

    class LevelIntro(layer.ColorLayer):

        def __init__(self, name, desc, r, g, b, a, width=None, height=None):
            super().__init__(r, g, b, a, width=width, height=height)
            self.title = cocos.text.Label(name, font_size=40, anchor_x="center", anchor_y="center")
            self.desc = cocos.text.Label(desc, font_size=30, anchor_x="center", anchor_y="center")
            self.title.x = self.width / 2
            self.title.y = self.height * 0.55
            self.desc.x = self.width / 2
            self.desc.y = self.height * 0.4
            self.add(self.title, z=3)
            self.add(self.desc, z=3)


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
        self.scroller.add(self.gridLayer, z=1)
        #self.scroller.add(self.bgLayer, z=-5)
        self.add(self.bgLayer, z=-5)

        self.scroller.viewport = cocos.rect.Rect(0, int(resheight * 0.12), int(reswidth), int(resheight * 0.78))
        self.add(self.scroller)
        
        self.intro = self.LevelIntro("Level Editor", self.level.name, 0, 0, 0, 0)
        self.add(self.intro, z=5)

        self.headerLayer = layer.ColorLayer(0, 0, 0, 175, width=int(reswidth), height=int(resheight * 0.1))
        self.headerLayer.x = 0
        self.headerLayer.y = resheight - self.headerLayer.height

        self.title = text.Label("Level Editor", font_name=resources.font[1], font_size=50, anchor_y="center", anchor_x="center")
        self.title.x = int(self.headerLayer.width / 2)
        self.title.y = int(self.headerLayer.height / 2)
        self.backButton = elements.mediumButton("BACK", events.mainmenuevents.onPlayButtonClick)
        self.backButton.x = int(self.headerLayer.width * 0.1)
        self.backButton.y =  int(self.headerLayer.height / 2)
        self.saveButton = elements.mediumButton("SAVE", events.mainmenuevents.backToMainMenu)
        self.saveButton.x = int(self.headerLayer.width * 0.9)
        self.saveButton.y =  int(self.headerLayer.height / 2)
        #self.editButton
        self.add(self.headerLayer, z=2)
        self.headerLayer.add(self.title)
        self.headerLayer.add(self.saveButton)
        self.headerLayer.add(self.backButton)

        self.footerLayer = layer.ColorLayer(0, 0, 0, 125, width=int(reswidth), height=int(resheight * 0.12))
        self.footerLayer.x = 0
        self.footerLayer.y = 0
        self.add(self.footerLayer, z=2)

        self.intro.do(cocos.actions.FadeIn(0.1) + cocos.actions.Delay(3) + cocos.actions.FadeOut(1))
        self.intro.title.do(cocos.actions.FadeOut(0.1) + cocos.actions.Delay(0.5) + cocos.actions.FadeIn(0.5) + cocos.actions.Delay(1.5) + cocos.actions.FadeOut(1))
        self.intro.desc.do(cocos.actions.FadeOut(0.1) + cocos.actions.Delay(1) + cocos.actions.FadeIn(0.5) + cocos.actions.Delay(1) + cocos.actions.FadeOut(1))



# * cocos.tiles.load has a function names save_xml(), which saves the loaded folder to xml
# * Along with the ability to change the shown tile directly on the layer and have it reflect in the game, this can be used for level editor
# * items.itempacks now has loaded resource and tile objects for each item in an item pack. This can be used to directly change data in the tileset.
# * However, care must be taken to find if the item is not in the level's required, that is it added there, otherwise the level will not work at all
# * This can be done by finding the res class in the item pack's item_res dictionary, and adding it to the level's required list as a tuple
# * This check can be done when an item is changed on the level 

# ! Cocos level renderer can be refreshed by set_dirty()
# ! This should only be done when cells have been changed, because it causes a performance hit