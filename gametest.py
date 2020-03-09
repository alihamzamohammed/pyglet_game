import cocos
import pyglet
import sys
import os
from pyglet.window import key as k
from cocos.scene import *
from cocos.layer import *
from cocos import tiles, actions, mapcolliders
import cfg
import pause
path = os.getcwd()

pyglet.resource.path.append(path + "\\items\\default")
pyglet.resource.path.append(path + "\\levels")
pyglet.resource.reindex()

class PlatformerController(actions.Action):
    on_ground = True
    MOVE_SPEED = 200
    JUMP_SPEED = 800
    GRAVITY = -1200
    SLOWDOWN = 0.1 * MOVE_SPEED
    slowdownthreshold = [0, 0]
    active = False
    slowdown = False

    def start(self):
        self.target.velocity = (0, 0)

    def step(self, dt):
        global keyboard, scroller
        if dt > 0.1:
            return
        vx, vy = self.target.velocity

        if not self.slowdown:
            if keyboard[k.RIGHT] > 0 or keyboard[k.LEFT] > 0:
                self.active = True
                self.slowdown = False
            else:
                self.active = False
                self.slowdown = True

            if self.active:
                vx = (keyboard[k.RIGHT] - keyboard[k.LEFT]) * self.MOVE_SPEED
                if self.slowdownthreshold[0] < 0.9:
                    self.slowdownthreshold[0] += 0.1
        else:
            if not self.slowdownthreshold[0] == 0:
                self.slowdownthreshold[1] = self.slowdownthreshold[0]
                self.slowdownthreshold[0] = 0
            if keyboard[k.RIGHT] > 0 or keyboard[k.LEFT] > 0:
                self.active = True
                self.slowdown = False
            elif vx == 0:
                self.slowdown = False
                self.slowdownthreshold[1] = 0
            elif vx > 0:
                vx -= (self.SLOWDOWN / self.slowdownthreshold[1])
                if vx < 0:
                    vx = 0
            elif vx < 0:
                vx += (self.SLOWDOWN / self.slowdownthreshold[1])
                if vx > 0:
                    vx = 0

        vy += self.GRAVITY * dt
        if self.on_ground and keyboard[k.SPACE]:
            vy = self.JUMP_SPEED

        dx = vx * dt
        dy = vy * dt

        last = self.target.get_rect()

        new = last.copy()
        new.x += dx
        new.y += dy

        self.target.velocity = self.target.collision_handler(last, new, vx, vy)

        self.on_ground = (new.y == last.y)

        self.target.position = new.center

        scroller.set_focus(*new.center)

def loadMap(level):
    global scroller
    try:
        player_layer = ScrollableLayer()
        player = cocos.sprite.Sprite("player.png")
        player_layer.add(player)
        player.do(PlatformerController())
        scroller = ScrollingManager()

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
        print("An exception was caught rendering the provided level\n Exception:", str(e))

class scene(Scene):

    is_event_handler=True

    class intro(ColorLayer):

        def __init__(self, r, g, b, a, width=None, height=None):
            super().__init__(r, g, b, a, width=width, height=height)
            self.lbl = cocos.text.Label("Test Level", font_size=40, anchor_x="center", anchor_y="center")
            self.lbl.x = self.width / 2
            self.lbl.y = self.height / 2
            self.add(self.lbl, z=3)

    def __init__(self, level):
        super().__init__()
        global scroller
        loadMap(level)
        self.add(ColorLayer(100, 120, 150, 255), z=0)
        self.add(scroller, z=1)
        i = self.intro(0, 0, 0, 0)
        self.add(i, z=2)
        i.do(cocos.actions.FadeIn(0.1) + cocos.actions.Delay(3) + cocos.actions.FadeOut(1))
        i.lbl.do(cocos.actions.FadeOut(0.1) + cocos.actions.Delay(0.5) + cocos.actions.FadeIn(0.5) + cocos.actions.Delay(1) + cocos.actions.FadeOut(1))

    def on_key_press(self, key, modifiers):
        print("Key event handled")
        if key == k.P:
            print("P key pressed")
            self.add(pause.pauseScreen)

keyboard = k.KeyStateHandler()
cocos.director.director.window.push_handlers(keyboard)