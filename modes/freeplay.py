import cocos
import pyglet
from cocos import *
from pyglet.window import key as k
from renderer import scroller, keyboard

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
        # PROBLEM: Sets focus on centre for scroller, means scroller is always centered on player position.
        # !: Need to find another solution for this
        # FIX: This code is now in another module, and is importing the required modules from renderer.

def main():
    return PlatformerController()
    # FIX: The main subroutine is called by the game, and is supposed to return the class for game level rendering, as well as be able to run any additional initialisation code required by the game mode.