import cocos
import pyglet
import sys
import os
from pyglet.window import key as k
from cocos.scene import *
from cocos.layer import *
from cocos import tiles, actions, mapcolliders
from xml import etree as et
import cfg
import pause
import logger
import events
path = os.getcwd()

pyglet.resource.path.append(path + "\\items\\default")
pyglet.resource.path.append(path + "\\levels")
pyglet.resource.reindex()

def loadLvl(level, gamemode):
    global scroller
    try:
        player_layer = ScrollableLayer()
        player = cocos.sprite.Sprite("player.png")
        player_layer.add(player)
        player.do(gamemode)

        fullmap = tiles.load(level)

        tilemap_walls = fullmap["walls"]
        tilemap_decorations = fullmap["decorations"]
        scroller.add(tilemap_decorations, z=-1)
        scroller.add(tilemap_walls, z=0)
        scroller.add(player_layer, z=1)

        start = tilemap_walls.find_cells(player_start=True)[0]
        r = player.get_rect()

        r.midbottom = start.midbottom

        player.position = r.center

        mapcollider = mapcolliders.RectMapCollider(velocity_on_bump="slide")
        player.collision_handler = mapcolliders.make_collision_handler(mapcollider, tilemap_walls)

    except Exception as e:
        # TODO: logger.addLog("An error was caught rendering the level.\n" + e, logger.loglevel["error"])
        print(e)

class scene(Scene):

    is_event_handler=True

    class intro(ColorLayer):

        def __init__(self, r, g, b, a, width=None, height=None):
            super().__init__(r, g, b, a, width=width, height=height)
            self.lbl = cocos.text.Label("Test Level", font_size=40, anchor_x="center", anchor_y="center")
            self.lbl.x = self.width / 2
            self.lbl.y = self.height / 2
            self.add(self.lbl, z=3)

    def __init__(self, level, gamemode):
        super().__init__()
        events.mainmenuevents.push_handlers(self.showMainMenu)
        global scroller
        loadLvl(level, gamemode)
        self.add(ColorLayer(100, 120, 150, 255), z=0)
        self.add(scroller, z=1)
        i = self.intro(0, 0, 0, 0)
        self.add(i, z=2)
        self.add(pause.pauseScreen, z=10)
        i.do(cocos.actions.FadeIn(0.1) + cocos.actions.Delay(3) + cocos.actions.FadeOut(1))
        i.lbl.do(cocos.actions.FadeOut(0.1) + cocos.actions.Delay(0.5) + cocos.actions.FadeIn(0.5) + cocos.actions.Delay(1) + cocos.actions.FadeOut(1))

    def showMainMenu(self):
        for child in self.get_children():
            self.remove(child) # FIX: This is a hopeful fix to the lag and duplication issues. By removing all children from the scene, it should help, as cocos should handle garbage collection


scroller = ScrollingManager()
keyboard = k.KeyStateHandler()
cocos.director.director.window.push_handlers(keyboard)