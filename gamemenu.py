import cocos
import pyglet
import os
import logger
import resources
from cocos.director import director
from cocos.scene import Scene
from cocos.layer import *
from cocos.actions import *
from cocos.sprite import *
from cocos.text import *
import levels
import modes
import elements # TODO: All elements in this class will be moved over, maybe?

x, y = director.window.width, director.window.height

title = cocos.text.Label(
    "Game Title",
    font_name=resources.font[1],
    font_size=50,
    anchor_y="top",
    anchor_x="left"
)

class GameMenu(Scene):

    def __init__(self):
        super().__init__()
        global x, y, title
        title.position = x * 0.04, y * 0.94
        self.add(title)
        modeBoxes = []
        for modeName, mode in modes.gamemodes.items():
            modeBox = GameModeBox(mode)
            modeBoxes.append(modeBox)
        for i in range(len(modeBoxes)):
            modeBoxes[i].x = ((x * 0.8) // 4) * (((i + 1) / 4) - ((i) // 4)) * 4
            modeBoxes[i].y = y * (0.6 - (i // 4) * 0.47)
            modeBoxes[i].delay = 2 + i
            self.add(modeBoxes[i])
            for child in modeBoxes[i].get_children():
                child.do(FadeOut(0.01) + Delay(modeBoxes[i].delay / 4) + FadeIn(0.5))

            #modeBoxes[i].do(Delay(0.1 + (i / 2)) + FadeIn(0.5))

    def on_enter(self):
        super().on_enter()


class GameModeSelection(Layer):
     
    def __init__(self):
        super().__init__()
        # global x, y
        # for modeName, mode in modes.gamemodes.items():
        #     modeBox = GameModeBox()
        #     modeBox.position = (x * 0.18) + (self.width / 2), y * 0.4
        #     self.add(modeBox)    

class LevelSelection(Layer):
    pass


class LevelBox(Layer):

    class ExtendedInfo(Layer):
        pass

class GameModeBox(Layer):

    def __init__(self, gameMode):
        super().__init__()
        bg = Sprite("gameBox.png")
        thumbnail = Sprite(gameMode.thumbnail)
        self.width = bg.width
        self.height = bg.height
        thumbnail.x = self.x
        thumbnail.y = self.y * 0.6
        gmTitle = Label(gameMode.name)
        gmTitle.x = self.x / 2
        gmTitle.y = self.y * 0.1
        self.delay = 0
        self.add(thumbnail, z=1)
        self.add(gmTitle, z=1)
        self.add(bg, z=0)
    
    #def on_enter(self):
    #    super().on_enter()

    class ExtendedInfo(Layer):
        pass







"""     class GameMenu(Scene):

    def __init__(self):
        super().__init__()
        # TODO: Get started on this section. Plan how to place game mode and level boxes, and how to animate between them.
        # TODO: Levels come first, with clickable boxes to select that level, and info screens that popup a larger info screen, with expanded thumbnail, metadata, and icons
        # TODO: On this screen will be button to lead to level creator/editor. If a level is selected, button will say 'edit', otherwise 'create' if no level is selected.
        # TODO: If level has a 'no edit' flag, level edit button will say 'edit', but will be greyed out.
        # TODO: After level is selected, a 'choose this level' button will animate the entire screen to move up to reveal game mode selection screen, same layout as level selection.
        # TODO: Level selected is shown as a box at the top of the screen
        # TODO: User can select level chosen box to switch levels.
        # TODO: Some levels can disallow certain gamemodes, those gamemodes will either be greyed out if found, or not visible. Greyed out preferred.

        # ! Before this, develop items, levels, and then game modes, IN THAT ORDER
        # ! And possibly level editor and level player

class LevelSelection(Layer):
    # ? levelsAdded = {}
    # ? x = 1
    # ? for level in levels:
    # ?     levelsAdded[level.name] = LevelBox(level)
    # ?     self.add(levelsAdded[level.name], x)
    # ?     x += 1
    pass

class GameModeSelection(Layer):
    # ? gamemodesAdded = {}
    # ? x = 1
    # ? for gamemode in gamemodes:
    # ?     gamemodesAdded[gamemode.name] = GameModeBox(gamemode)
    # ?     self.add(gamemodesAdded[gamemode.name], x)
    # ?     x += 1
    pass

class LevelBox(Layer):

    class ExtendedInfo(Layer):
        pass

class GameModeBox(Layer):

    class ExtendedInfo(Layer):
        pass """