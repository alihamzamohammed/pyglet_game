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
import levels
import modes
path = os.getcwd()

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
    global bgLayer
    try:
        fullmap = tiles.load(level.datapath)
        tilemap_walls = fullmap["walls"]
        tilemap_decorations = fullmap["decorations"]

        scroller.add(bgLayer, z=-2)
        scroller.add(tilemap_decorations, z=-1)
        scroller.add(tilemap_walls, z=0)
        scroller.add(player_layer, z=1)
        
        start = tilemap_walls.find_cells(player_start=True)[0]
        r = player.get_rect()
        r.midbottom = start.midbottom
        player.position = r.center
        
        mapcollider = mapcolliders.RectMapCollider(velocity_on_bump="slide")
        player.collision_handler = mapcolliders.make_collision_handler(mapcollider, tilemap_walls)
        
        gamemoderun = player.do(gamemode.main())

    except Exception as e:
        # TODO: 
        logger.addLog("An error was caught rendering the level.\n" + str(e), logger.loglevel["error"])
        #raise e
      #  import events
       # events.mainmenuevents.backToMainMenu()
     #   print(e)

class Renderer(Scene):

    is_event_handler=True
    class LevelIntro(ColorLayer):

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

    def __init__(self, level, gamemode):
        super().__init__()
        self.level = level
        self.gamemode = gamemode
        if not isinstance(self.level, levels.Level):
            return None
        events.mainmenuevents.push_handlers(self.mainMenuIsShowing)
        events.pausescreenevents.push_handlers(self.pauseScreenNotShowing, self.pauseScreenShowing)
        global scroller
        global bgLayer
        if isinstance(level.background, str):
            bgLayer = ScrollableLayer()
            bgLayer.parallax = 0.5
            bgImage = cocos.sprite.Sprite(level.background)
            # TODO: Add code to scale image to viewport, then tile it
            bgLayer.add(bgImage)
        elif isinstance(level.background, tuple):
            self.add(ColorLayer(level.background[0], level.background[1], level.background[2], level.background[3]), z=0)
        self.add(scroller, z=1)
        self.intro = self.LevelIntro(level.name, gamemode.name, 0, 0, 0, 0)
        self.add(self.intro, z=2)
        loadLvl(self.level, self.gamemode.module)
        self.add(pause.pauseScreen, z=10)
        pause.pauseScreen.mainMenu = False
        self.intro.do(cocos.actions.FadeIn(0.1) + cocos.actions.Delay(3) + cocos.actions.FadeOut(1))
        self.intro.title.do(cocos.actions.FadeOut(0.1) + cocos.actions.Delay(0.5) + cocos.actions.FadeIn(0.5) + cocos.actions.Delay(1.5) + cocos.actions.FadeOut(1))
        self.intro.desc.do(cocos.actions.FadeOut(0.1) + cocos.actions.Delay(1) + cocos.actions.FadeIn(0.5) + cocos.actions.Delay(1) + cocos.actions.FadeOut(1))

    def mainMenuIsShowing(self):
        if not self.get_children() == []:
            global fullmap
            global scroller
            global player
            global gamemoderun
            player.remove_action(gamemoderun)
            for child in scroller.get_children():
                scroller.remove(child)
            fullmap = None
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