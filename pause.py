import cocos
import pyglet
from cocos.layer import *
from cocos.text import *
from cocos.sprite import *
from cocos.actions import *
import elements
import resources
from pyglet.window import key as k

class PauseScreen(ColorLayer):

    is_event_handler = True

    def __init__(self, r, g, b, a, width=None, height=None):
        x, y = cocos.director.director.get_window_size()
        super().__init__(r, g, b, a, width=width, height=height)
        self.title = Label("Paused", font_size=50, anchor_x="center", anchor_y="center", font_name=resources.font)
        self.title.x = x / 2
        self.title.y = y * 0.72
        self.opacity = 100
        self.add(self.title)
        self.isvisible = False
        self.do(FadeOut(0.01))

    def on_key_press(self, key, modifiers):
        if key == k.P:
            if not self.isvisible:
                self.do(FadeTo(100, 0.5)) # PROBLEM: FadeIn and FadeOut affect opacity of the target class, in this case PauseScreen, prventing it from being translucent.
                                          # FIX: Solved by using FadeTo to fade to a specific alpha value
            else:
                self.do(FadeTo(0, 0.5))
            self.isvisible = not self.isvisible

pauseScreen = PauseScreen(0, 0, 0, 100)