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

    def __init__(self, width=None, height=None):
        super().__init__(0, 0, 0, 50, width=width, height=height)
        self.title = Label("Paused", font_size=50, anchor_x="center", anchor_y="center", font_name=resources.font)
        self.title.x = self.width / 2
        self.title.y = self.height * 0.72
        self.add(self.title)

    def on_key_press(self, key, modifiers):
        if self.visible and key == k.symbol_string(k.ESCAPE):
            self.parent.remove(self)

    def on_enter(self):
        super().on_enter()
        self.do(FadeIn(1))

    def on_exit(self):
        self.do(FadeOut(1))
        super().on_exit()

pauseScreen = PauseScreen()