import pyglet
from cocos import *
import importlib
import os
from pyglet.window import key as k
from renderer import scroller, keyboard
import cfg

class PlatformerController(actions.Action):

    on_ground = True
    MOVE_SPEED = 200
    JUMP_SPEED = 600
    GRAVITY = -1200
    SLOWDOWN = 0.1 * MOVE_SPEED
    slowdownthreshold = [0, 0]
    active = False
    slowdown = False
    global RIGHTKEY, LEFTKEY, JUMPKEY
    RIGHTKEY = cfg.keyConfig["right"]
    LEFTKEY = cfg.keyConfig["left"]
    JUMPKEY = cfg.keyConfig["jump"]

    def start(self):
        import items as i
        for itemPack in cfg.loadedLevel.required["itempack"]:
            if "sourcecode" in i.itempacks[itemPack].required:
                for ipSource in i.itempacks[itemPack].required["sourcecode"]:
                    module = importlib.import_module("items." + i.itempacks[itemPack].idx + "." + ipSource[:-3])
                    if "bounce_modifier" in dir(module):
                        self.bounce = module.bounce_modifier(self.bounce)

        self.target.velocity = (0, 0)
        from renderer import fullmap

    def step(self, dt):
        global keyboard, scroller
        if dt > 0.1:
            return
        vx, vy = self.target.velocity

        if not self.slowdown:
            if keyboard[RIGHTKEY] > 0 or keyboard[LEFTKEY] > 0:
                self.active = True
                self.slowdown = False
            else:
                self.active = False
                self.slowdown = True

            if self.active:
                vx = (keyboard[RIGHTKEY] - keyboard[LEFTKEY]) * self.MOVE_SPEED
                if self.slowdownthreshold[0] < 0.9:
                    self.slowdownthreshold[0] += 0.1
        else:
            if not self.slowdownthreshold[0] == 0:
                self.slowdownthreshold[1] = self.slowdownthreshold[0]
                self.slowdownthreshold[0] = 0
            if keyboard[RIGHTKEY] > 0 or keyboard[LEFTKEY] > 0:
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
        vy = self.bounce(self.JUMP_SPEED, vy)


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

    def bounce(self, value, original):
        global JUMPKEY
        if self.on_ground and keyboard[JUMPKEY]:
            return value
        else:
            return original

    def move(self, key, value):
        pass

def main():
    return PlatformerController()

name = "Free Play"
desc = "A game mode for freely roaming the level."

# ~: Game modes can use the main() subroutine to run other subroutines and init other sprites and make them do stuff. Here, because scroller is imported,
# ~: the game mode can add as many layers as it wants to the scroller, and they will render and display to the player, without any modification to renderer.py, or having to globalise and import more classes.
# ~: Sprites and layers can be added to scroller when start() runs, which marks the official start of the renderer displaying things
# ~: This allows for almost unlimited functionality to be added.