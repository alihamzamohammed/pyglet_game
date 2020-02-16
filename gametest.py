import cocos
import pyglet
import sys
import os
from pyglet.window import key
from cocos.scene import *
from cocos.layer import *
from cocos import tiles, actions, mapcolliders
path = os.getcwd()

pyglet.resource.path.append(path + "\\items\\default")
pyglet.resource.path.append(path + "\\levels")
pyglet.resource.reindex()

class PlatformerController(actions.Action):
    on_ground = True
    MOVE_SPEED = 200
    JUMP_SPEED = 800
    GRAVITY = -1200

    def start(self):
        self.target.velocity = (0, 0)

    def step(self, dt):
        global keyboard, scroller
        if dt > 0.1:
            return
        vx, vy = self.target.velocity

        vx = (keyboard[key.RIGHT] - keyboard[key.LEFT]) * self.MOVE_SPEED
        vy += self.GRAVITY * dt
        if self.on_ground and keyboard[key.SPACE]:
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

player_layer = ScrollableLayer()
player = cocos.sprite.Sprite("player.png")
player_layer.add(player)
player.do(PlatformerController())

scroller = ScrollingManager()
fullmap = tiles.load("levels/test.xml")
tilemap_walls = fullmap["walls"]
scroller.add(tilemap_walls, z=0)
scroller.add(player_layer, z=1)

start = tilemap_walls.find_cells(player_start=True)[0]
r = player.get_rect()

r.midbottom = start.midbottom

player.position = r.center

mapcollider = mapcolliders.RectMapCollider(velocity_on_bump="slide")
player.collision_handler = mapcolliders.make_collision_handler(mapcollider, tilemap_walls)

scene = Scene()
scene.add(ColorLayer(100, 120, 150, 255), z=0)
scene.add(scroller, z=1)

keyboard = key.KeyStateHandler()
cocos.director.director.window.push_handlers(keyboard)

def on_key_press(key, modifier):
    if key == pyglet.window.key.D:
        tilemap_walls.set_debug(True)
cocos.director.director.window.push_handlers(on_key_press)