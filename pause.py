import cocos
import pyglet
from cocos.layer import *
from cocos.text import *
from cocos.sprite import *
from cocos.actions import *
import elements
import resources
import events
import cfg
from pyglet.window import key as k

class PauseScreen(ColorLayer):

    is_event_handler = True

    def __init__(self, r, g, b, a, width=None, height=None):
        x, y = cocos.director.director.get_window_size()
        super().__init__(r, g, b, a, width=width, height=height)
        self.title = Label("Paused", font_size=50, anchor_x="center", anchor_y="center", font_name=resources.font)
        self.title.x = x / 2
        self.title.y = y * 0.72

        self.quitButton = elements.MainMenuButton("Quit Level", events.mainmenuevents.backToMainMenu, 3, False)
        self.resumeButton = elements.MainMenuButton("Resume Game", self.resumeGame, 2, False)

        self.opacity = 150
        self.isvisible = False
        self.mainMenu = False

        self.add(self.title)
        self.add(self.quitButton)
        self.add(self.resumeButton)

        self.elementFadeOut(0.01)
        events.mainmenuevents.push_handlers(self.showMainMenu)

    def on_key_press(self, key, modifiers):
        if key == k.P:
            if not self.isvisible:
                self.elementFadeIn(0.5)
                events.pausescreenevents.onPauseScreenAppear()
            else:
                self.elementFadeOut(0.5)
                if not self.mainMenu:
                    events.pausescreenevents.onPauseScreenDisappear()
            self.isvisible = not self.isvisible

    def showMainMenu(self):
        self.isvisible = False
        self.mainMenu = True
        self.elementFadeOut(0.01)
        cfg.loadedLevel = None
        cfg.loadedGameMode = None
        # ?: With the new event "mainMenuShowing", this may not need to be here, as the fade is taken care of by the scene transition anyways, at which point the pause menu will be removed from the renderer anyways

    def resumeGame(self):
        self.elementFadeOut(0.5)
        if not self.mainMenu:
            events.pausescreenevents.onPauseScreenDisappear()
        self.isvisible = False

    def elementFadeIn(self, duration):
        self.do(FadeTo(150, duration))
        self.title.do(FadeIn(duration))
        for el in self.get_children():  
            list(map(lambda element: element.do(FadeIn(duration)), el.get_children()))

    def elementFadeOut(self, duration):
        self.do(FadeTo(0, duration))
        self.title.do(FadeOut(duration))
        for el in self.get_children():
            list(map(lambda element: element.do(FadeOut(duration)), el.get_children()))

pauseScreen = PauseScreen(0, 0, 0, 150)