import pyglet
import cocos
from cocos import tiles, text, sprite, layer, scene, batch, rect
from cocos.director import director
import xml.etree.ElementTree as et
import levels
import items
import logger
import cfg
import resources
import elements
import events
import scaling as sc

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
        self.initialCell = None
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
        if x < 0 or y < 0: return
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
            self.initialCell = self.hovered
            if x < 0 or y < 0: return
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
            cell = self.gridList[x // 32][y // 32]
            if x < 0 or y < 0: return
            if not cell in self.dragging:
                if cell == self.initialCell: return
                if cell[1]:
                    cell[0].image = pyglet.resource.image("leveleditorItem.png")
                    cell[1] = False
                    self.dragging.append(cell)
                else:
                    cell[0].image = pyglet.resource.image("leveleditorItemClicked.png")
                    cell[1] = True                    
                    self.dragging.append(cell)
        except IndexError:
            pass

    def on_mouse_release(self, x, y, buttons, modifiers):
        self.dragging = []
        self.initialCell = None

    # TODO: Create more efficient object style cells instead of lists
    # TODO: Add object properties automatically changing picture on status (hover, click, drag?)
    # TODO: Fix 1st tile not selectable on drag

class LevelEditor(scene.Scene):

    is_event_handler = True

    class LevelEditorScrollManager(layer.ScrollingManager):

        def on_cocos_resize(self, usable_width, usable_height):
            w, h = sc.scale(self.viewport.width, self.viewport.height)
            #self.viewport = rect.Rect(self.viewport.x, self.viewport.y, w, h)
            #super().on_cocos_resize(usable_width, usable_height)
            self.update_view_size()
            self.refresh_focus()


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

        self.intro = self.LevelIntro("Level Editor", self.level.name, 0, 0, 0, 0)
        self.add(self.intro, z=5)

        self.intro.do(cocos.actions.FadeIn(0.1))
        self.intro.title.do(cocos.actions.FadeOut(0.1) + cocos.actions.Delay(0.5) + cocos.actions.FadeIn(0.5))
        self.intro.desc.do(cocos.actions.FadeOut(0.1) + cocos.actions.Delay(1) + cocos.actions.FadeIn(0.5) + cocos.actions.CallFunc(self.loadSceenShowing))
        
    def loadSceenShowing(self):
        self.levelData = tiles.load(self.level.datapath)
        self.tilemap_decorations = self.levelData["decorations"]
        self.tilemap_walls = self.levelData["walls"]
        if isinstance(self.level.background, str):
            self.bgLayer = layer.ScrollableLayer()
            self.bgLayer.parallax = 0.5
            bgImage = cocos.sprite.Sprite(self.level.background)
            # TODO: Add code to scale image to viewport, then tile it
            self.bgLayer.add(bgImage)


        viewport = rect.Rect(0, int(resheight * 0.12), int(reswidth), int(resheight * 0.76))
        self.scroller = self.LevelEditorScrollManager(viewport, True)
        self.scroller.autoscale = False
        #self.scroller.on_cocos_resize = on_cocos_resize
        self.scroller.scale = 1
        self.scroller.viewport = cocos.rect.Rect(0, int(resheight * 0.12), int(reswidth), int(resheight * 0.76))
        #self.scroller.x = 0
        #self.scroller.y = 0
        self.scroller.add(self.tilemap_decorations, z=-1)
        self.scroller.add(self.tilemap_walls, z=0)
        self.gridLayer = LevelGridLayer(walls=self.tilemap_walls, decorations=self.tilemap_decorations, scroller=self.scroller, level=self.level)
        self.scroller.add(self.gridLayer, z=1)
        self.add(self.bgLayer, z=-5)

        self.add(self.scroller)
        
        self.headerLayer = layer.ColorLayer(0, 0, 0, 175, width=int(reswidth), height=int(resheight * 0.12))
        self.headerLayer.x = 0
        self.headerLayer.y = resheight - self.headerLayer.height

        self.title = text.Label("Level Editor", font_name=resources.font[1], font_size=50, anchor_y="center", anchor_x="center")
        self.title.x = int(self.headerLayer.width / 2)
        self.title.y = int(self.headerLayer.height / 2)
        
        self.backButton = elements.mediumButton("BACK", events.mainmenuevents.onPlayButtonClick)
        self.backButton.x = int(self.headerLayer.width * 0.065)
        
        self.backButton.y =  int(self.headerLayer.height / 2)
        self.saveButton = elements.mediumButton("SAVE", events.mainmenuevents.backToMainMenu)
        
        self.saveButton.x = int(self.headerLayer.width * 0.947)
        self.saveButton.y =  int(self.headerLayer.height / 2)
        
        #self.editButton
        self.add(self.headerLayer, z=2)
        
        self.headerLayer.add(self.title)
        self.headerLayer.add(self.saveButton)
        self.headerLayer.add(self.backButton)
        
        self.backButton.px = self.saveButton.px = self.headerLayer.x
        self.backButton.py = self.saveButton.py = self.headerLayer.y
        
        self.backButton.show(0.1)
        self.saveButton.show(0.1)

        self.footerLayer = layer.ColorLayer(0, 0, 0, 125, width=int(reswidth), height=int(resheight * 0.12))
        self.footerLayer.x = 0
        self.footerLayer.y = 0
        self.add(self.footerLayer, z=2)
        
        self.upButton = elements.smallButton("\u2b9d", self.moveUp)
        self.rightButton = elements.smallButton("\u2b9e", self.moveRight)
        self.leftButton = elements.smallButton("\u2b9c", self.moveLeft)
        self.downButton = elements.smallButton("\u2b9f", self.moveDown)
        
        self.upButton.x = self.footerLayer.width * 0.92
        self.upButton.y = self.footerLayer.height * 0.75
        
        self.rightButton.x = self.footerLayer.width * 0.955
        self.rightButton.y = self.footerLayer.height * 0.5
        
        self.leftButton.x = self.footerLayer.width * 0.885
        self.leftButton.y = self.footerLayer.height * 0.5
        
        self.downButton.x = self.footerLayer.width * 0.92
        self.downButton.y = self.footerLayer.height * 0.25
        
        self.footerLayer.add(self.upButton)
        self.footerLayer.add(self.rightButton)
        self.footerLayer.add(self.leftButton)
        self.footerLayer.add(self.downButton)
        
        self.upButton.show(0.1)
        self.rightButton.show(0.1)
        self.leftButton.show(0.1)
        self.downButton.show(0.1)        


        self.scroller.set_focus(int(self.tilemap_walls.view_w / 2), int(self.tilemap_walls.view_h / 2))
        self.scrollerFocusLimits = {"up": 0, "down": int(self.tilemap_walls.view_h / 2), "left": int(self.tilemap_walls.view_w / 2), "right": 0}

        self.intro.do(cocos.actions.Delay(3) + cocos.actions.FadeOut(1))
        self.intro.title.do(cocos.actions.Delay(3) + cocos.actions.FadeOut(1))
        self.intro.desc.do(cocos.actions.Delay(3) + cocos.actions.FadeOut(1))

    def moveUp(self):
        self.scroller.set_focus(self.scroller.fx, self.scroller.fy + 10)

    def moveRight(self):
        self.scroller.set_focus(self.scroller.fx + 10, self.scroller.fy)
    
    def moveLeft(self):
        if self.scroller.fx >= self.scrollerFocusLimits["left"] + 1:
            self.scroller.set_focus(self.scroller.fx - 10, self.scroller.fy)

    def moveDown(self):
        if self.scroller.fy >= self.scrollerFocusLimits["down"] + 1:
            self.scroller.set_focus(self.scroller.fx, self.scroller.fy - 10)

# * cocos.tiles.load has a function names save_xml(), which saves the loaded folder to xml
# * Along with the ability to change the shown tile directly on the layer and have it reflect in the game, this can be used for level editor
# * items.itempacks now has loaded resource and tile objects for each item in an item pack. This can be used to directly change data in the tileset.
# * However, care must be taken to find if the item is not in the level's required, that is it added there, otherwise the level will not work at all
# * This can be done by finding the res class in the item pack's item_res dictionary, and adding it to the level's required list as a tuple
# * This check can be done when an item is changed on the level 

# ! Cocos level renderer can be refreshed by set_dirty()
# ! This should only be done when cells have been changed, because it causes a performance hit