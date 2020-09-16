import cocos
import pyglet
import os
import logger
import resources
import cfg
from cocos.director import director
from cocos.scene import Scene
from cocos.layer import *
from cocos.actions import *
from cocos.sprite import *
from cocos.text import *
import levels
import modes
import events
import elements # TODO: All elements in this class will be moved over, maybe?

import scaling as sc

x, y = director.window.width, director.window.height
reswidth, resheight = [int(res) for res in cfg.configuration["Core"]["defaultres"].split("x")]

title = cocos.text.Label(
    "Game Modes",
    font_name=resources.font[1],
    font_size=50,
    anchor_y="top",
    anchor_x="left"
)

"""Small button. A button for placing in small spaces, or to activate non-crucial functions"""
class smallButton(Layer):

    is_event_handler = True

    def __init__(self, label, eventName, active = False, *args, **kwargs):
        super().__init__()
        global x, y

        self.eventName = eventName
        self.active = active
        if eventparam in *args:
            self.eventparam = *args.eventparam

        self.bgImage = Sprite("smallButton.png")
        self.lbl = Label(label, anchor_x="center", anchor_y="center", dpi=110, font_size=16)

        self.x = 0
        self.y = 0
        self.px = 0
        self.py = 0

        self.width_range = [int((self.px + self.x) - (self.bgImage.width / 2)), int((self.px + self.x) + (self.bgImage.width / 2))]
        self.height_range = [int((self.py + self.y) - (self.bgImage.height / 2)), int((self.py + self.y) + (self.bgImage.width / 2))]

        self.add(self.bgImage)
        self.add(self.lbl)

        self.schedule_interval(self.setWH, 1)
        self.resume_scheduler()

    def setWH(self, dt):
        x, y = director.window.width, director.window.height
        nmin = sc.scale(int((self.px + self.x) - (self.bgImage.width / 2)), int((self.py + self.y) - (self.bgImage.height / 2)))
        nmax = sc.scale(int((self.px + self.x) + (self.bgImage.width / 2)), int((self.py + self.y) + (self.bgImage.width / 2)))
        self.width_range = [int(nmin[0]), int(nmax[0])]
        self.height_range = [int(nmin[1]), int(nmax[1])]

    def on_mouse_motion(self, x, y, dx, dy):
        if self.active:
            self.bgImage.image = pyglet.resource.image("smallButtonClicked.png")
            self.lbl.element.color = (0, 0, 0, 255)
        elif x in range(self.width_range[0], self.width_range[1]) and y in range(self.height_range[0], self.height_range[1]):
            self.bgImage.image = pyglet.resource.image("smallButtonHovered.png")
            self.lbl.element.color = (255, 255, 255, 255)
        else:
            self.bgImage.image = pyglet.resource.image("smallButton.png")
            self.lbl.element.color = (255, 255, 255, 255)

    def on_mouse_press(self, x, y, buttons, modifiers):
        if x in range(self.width_range[0], self.width_range[1]) and y in range(self.height_range[0], self.height_range[1]):
            self.bgImage.image = pyglet.resource.image("smallButtonClicked.png")
            self.active = True
            self.lbl.element.color = (0, 0, 0, 255)
            if hasattr(self, "eventparam"):
                self.eventName(self.eventparam)
            else:
                self.eventName() 


class GameMenu(Scene):

    def __init__(self):
        super().__init__()
        global title
        title.position = reswidth * 0.04, resheight * 0.94
        self.add(title)
        modeBoxes = []
        for modeName, mode in modes.gamemodes.items():
            modeBox = GameModeBox(mode)
            modeBoxes.append(modeBox)
        for i in range(len(modeBoxes)):
            modeBoxes[i].x = ((reswidth * 0.8) // 4) * (((i + 1) / 4) - ((i) // 4)) * 4
            modeBoxes[i].y = resheight * (0.6 - (i // 4) * 0.47)
            modeBoxes[i].delay = 2 + i
            modeBoxes[i].update_positions()
            self.add(modeBoxes[i])
            for child in modeBoxes[i].get_children():
                child.do(FadeOut(0.01) + Delay(modeBoxes[i].delay / 4) + FadeIn(0.5))
                if isinstance(child, smallButton):
                    for child2 in child.get_children():
                            child2.do(FadeOut(0.01) + Delay(modeBoxes[i].delay / 4) + FadeIn(0.5))


            #modeBoxes[i].do(Delay(0.1 + (i / 2)) + FadeIn(0.5))

    def on_enter(self):
        super().on_enter()


# class GameModeSelection(Layer):
     
#     def __init__(self):
#         super().__init__()
#         # global x, y
#         # for modeName, mode in modes.gamemodes.items():
#         #     modeBox = GameModeBox()
#         #     modeBox.position = (x * 0.18) + (self.width / 2), y * 0.4
#         #     self.add(modeBox)    

# class LevelSelection(Layer):
#     pass


# class LevelBox(Layer):

#     class ExtendedInfo(Layer):
#         pass

class GameModeBox(Layer):

    def __init__(self, gameMode):
        super().__init__()
        self.gameMode = gameMode
        self.bg = Sprite("gameBox.png")
        self.thumbnail = Sprite(gameMode.thumbnail)
        self.thumbnail.scale_x = self.thumbnail.width / 200
        self.thumbnail.scale_y = self.thumbnail.height / 200
        self.infoButton = smallButton("i", events.gamemenuevents.showExtendedInfo, eventparam=gameMode.name)
        self.width = self.bg.width
        self.height = self.bg.height
        self.thumbnail.x = self.x
        self.thumbnail.y = self.y * 0.6
        self.gmTitle = Label(gameMode.name, color=(0, 0, 0, 255), font_size=20, anchor_x="left", anchor_y="center")
        self.gmTitle.x = self.x / 2
        self.gmTitle.y = self.y * 0.1
        self.delay = 0
        self.add(self.thumbnail, z=1)
        self.add(self.gmTitle, z=1)
        self.add(self.infoButton, z=1)
        self.add(self.bg, z=0)
    
    def update_positions(self):
        self.thumbnail.x = 0
        self.thumbnail.y = 20
        self.gmTitle.x = -100
        self.gmTitle.y = -104
        self.infoButton.x = 80
        self.infoButton.y = -107
        self.infoButton.px = self.x
        self.infoButton.py = self.y
        

    class ExtendedInfo(Layer):

        is_event_handler = True

        def __init__(self):
            super().__init__()
            events.gamemenuevents.push_handlers(self)
            self.infoBox = Sprite("infoBox.png")
            self.bgDimmer = ColorLayer(0, 0, 0, 100)
            self.bgDimmer.do(Hide())
            self.infoBox.do(Hide())


        def ExtendedInfoShow(self, name):
            if name == self.parent.gameMode.name:
                self.infoBox.do(FadeIn(1))
                self.bgDimmer.do(FadeIn(1))

        def ExtendedInfoHide(self, name):
            if name == self.parent.gameMode.name:
                self.infoBox.do(FadeOut(1))
                self.bgDimmer.do(FadeOut(1))