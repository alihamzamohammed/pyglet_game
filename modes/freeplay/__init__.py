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
    JUMP_SPEED = 800
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
        self.target.velocity = (0, 0)
        from renderer import fullmap
        #importlib.importmodule(scroller)

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
    import levels as l
    import items as i
    #l.levels[cfg.loadedLevel.idx]
    for itemPack in cfg.loadedLevel.required["itempack"]:
        print(itemPack)
        if "sourcecode" in i.itempacks[itemPack].required:
            for ipSource in i.itempacks[itemPack].required["sourcecode"]:
                #importlib.import_module
                print(os.getcwd() + "\\" + i.itempacks[itemPack].folder + "\\" + ipSource)
        
    return PlatformerController()

name = "Free Play"
desc = "A game mode for freely roaming the level."

# ~: Game modes can use the main() subroutine to run other subroutines and init other sprites and make them do stuff. Here, because scroller is imported,
# ~: the game mode can add as many layers as it wants to the scroller, and they will render and display to the player, without any modification to renderer.py, or having to globalise and import more classes.
# ~: Sprites and layers can be added to scroller when start() runs, which marks the official start of the renderer displaying things
# ~: This allows for almost unlimited functionality to be added.

# PROBLEM: To allow items to use custom code, they must be able to override code declared in game modes. For example, code for a trampoline needs to modify the gravity value when
# PROBLEM: detecting bounce on top of the trampoline. This will need extra code to check if the player is on top of the trampoline, and supply a modified gravity value if that is the case,
# PROBLEM: otherwise run the code as normal. This would mean delegating movement on each axis to its own subroutine, supplying required values through parameters, and using decorators to
# PROBLEM: modify the parameter when called. This could allow a bounce function to run with a modified value. In this way, game modes which choose to disable jumping can still do so.

# PROBLEM: This seems to be the best solution, but requires decorators to be declared even when the decorator function does not exist.

# TODO: EXAMPLE CODE:

# TODO: THIS IS CODE FROM ITEM PACK
# TODO: def bounce_modifier(call):
# TODO:     def bounce(func):
# TODO:         def inner(value):
# TODO:             if call.block_underneath == "trampoline":
# TODO:                 value = 2
# TODO:             elif call.block_underneath == "sponge":
# TODO:                 value = 0.5
# TODO:             else:
# TODO:                 value = 1
# TODO:             func(value)
# TODO:         return inner
# TODO:     return bounce

# TODO: from item_pack import *                   <-- This will override the default function, which does nothing

# TODO: bounce_modifier = lambda x: lambda y: y   <-- This is the function that will be overridden

# TODO: @bounce_modifier(self)
# TODO: def bounce(value):
# TODO:     vy += value * dt
# TODO:     if self.on_ground and keyboard[k.SPACE]:
# TODO:         vy = self.JUMP_SPEED

# TODO: bounce(self.GRAVITY)