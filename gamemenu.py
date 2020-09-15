import cocos
import pyglet
import os
import logger
from cocos.director import director
from cocos.scene import Scene
from cocos.layer import *
import levels
import modes
import elements # TODO: All elements in this class will be moved over, maybe?

x, y = director.window.width, director.window.height

class GameMenu(Scene):

    def __init__(self):
        super().__init__()
        global x, y
        title = elements.gameTitle
        title.position = x * 0.2, y * 0.8
        self.add(elements.gameTitle)


class GameModeSelection(Layer):
     
     pass

class LevelSelection(Layer):
    pass


class LevelBox(Layer):

    class ExtendedInfo(Layer):
        pass

class GameModeBox(Layer):

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