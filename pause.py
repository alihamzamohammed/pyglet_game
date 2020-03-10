import cocos
import pyglet
from cocos.layer import *
from cocos.text import *
from cocos.sprite import *
from cocos.actions import *
import elements
import resources
import events
from pyglet.window import key as k

class PauseScreen(ColorLayer):

    is_event_handler = True

    def __init__(self, r, g, b, a, width=None, height=None):
        x, y = cocos.director.director.get_window_size()
        super().__init__(r, g, b, a, width=width, height=height)
        self.title = Label("Paused", font_size=50, anchor_x="center", anchor_y="center", font_name=resources.font)
        self.title.x = x / 2
        self.title.y = y * 0.72

        self.quitButton = elements.MainMenuButton("Quit Level", events.mainmenuevents.backToMainMenu, 1, False)

        self.opacity = 150
        self.isvisible = False

        self.add(self.title)
        self.add(self.quitButton)

        self.do(FadeOut(0.01))
        self.title.do(FadeOut(0.01))
        (element.do(FadeOut(0.01)) for element in self.quitButton.get_children())

    def on_key_press(self, key, modifiers):
        if key == k.P:
            if not self.isvisible:
                self.do(FadeTo(150, 0.5))
                self.title.do(FadeIn(0.5))
                (element.do(FadeIn(0.5)) for element in self.quitButton.get_children())
            else:
                self.do(FadeTo(0, 0.5))
                self.title.do(FadeOut(0.5))
                (element.do(FadeOut(0.5)) for element in self.quitButton.get_children())
            self.isvisible = not self.isvisible

pauseScreen = PauseScreen(0, 0, 0, 150)