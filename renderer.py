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
from levels import levels
path = os.getcwd()

#pyglet.resource.path.append(path + "\\items\\default")
#pyglet.resource.path.append(path + "\\levels")
pyglet.resource.reindex()

def init():
    global scroller
    global player_layer
    global player
    player_layer = ScrollableLayer()
    player = cocos.sprite.Sprite("player.png")
    player_layer.add(player)
    scroller = ScrollingManager()

def loadLvl(level, gamemode):
    global scroller
    global player_layer
    global player
    global fullmap
    global gamemoderun
    global start
    global r
    global mapcollider
    global tilemap_decorations, tilemap_walls
    try:
        #player_layer = ScrollableLayer()
        #player = cocos.sprite.Sprite("player.png")
        #player_layer.add(player)
        gamemoderun = player.do(gamemode)

        fullmap = tiles.load(level.datapath)
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
            self.title = cocos.text.Label("lvl", font_size=40, anchor_x="center", anchor_y="center")
            self.desc = cocos.text.Label("desc", font_size=30, anchor_x="center", anchor_y="center")
            self.title.x = self.width / 2
            self.title.y = self.height * 0.55
            self.desc.x = self.width / 2
            self.desc.y = self.height * 0.4
            self.add(self.title, z=3)
            self.add(self.desc, z=3)

    def __init__(self, level, gamemode):
        super().__init__()
        self.level = level
        self.gamemode = gamemode
        if not isinstance(self.level, levels.Level):
            return None
        events.mainmenuevents.push_handlers(self.mainMenuIsShowing)
        events.pausescreenevents.push_handlers(self.pauseScreenNotShowing, self.pauseScreenShowing)
        global scroller
        self.add(ColorLayer(100, 120, 150, 255), z=0)
        self.add(scroller, z=1)
        self.i = self.intro(0, 0, 0, 0)
        self.i.title.element.text = level.name
        self.i.desc.element.text = str(gamemode)
        self.add(self.i, z=2)
        loadLvl(self.level, self.gamemode)
        self.add(pause.pauseScreen, z=10)
        self.i.do(cocos.actions.FadeIn(0.1) + cocos.actions.Delay(3) + cocos.actions.FadeOut(1))
        self.i.title.do(cocos.actions.FadeOut(0.1) + cocos.actions.Delay(0.5) + cocos.actions.FadeIn(0.5) + cocos.actions.Delay(1.5) + cocos.actions.FadeOut(1))
        self.i.desc.do(cocos.actions.FadeOut(0.1) + cocos.actions.Delay(1) + cocos.actions.FadeIn(0.5) + cocos.actions.Delay(1) + cocos.actions.FadeOut(1))

    def mainMenuIsShowing(self):
        if not self.get_children() == []:
            global fullmap
            global scroller
            global player
            #global player_layer
            global gamemoderun
            #global r
            #global mapcollider
            #global start
            #global tilemap_decorations, tilemap_walls
            player.remove_action(gamemoderun)
            for child in scroller.get_children():
                scroller.remove(child)
            fullmap = None
            # ?: These may not need to be deleted?
            # start = None
            # mapcollider = None
            # tilemap_walls = None
            # tilemap_decorations = None
            for child in self.get_children():
                self.remove(child)

    def pauseScreenShowing(self):
        global player
        player.pause()

    def pauseScreenNotShowing(self):
        global player
        player.resume()


keyboard = k.KeyStateHandler()
cocos.director.director.window.push_handlers(keyboard)