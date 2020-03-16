import cocos
import pyglet

class Item(cocos.tiles.Cell):

    def __init__(self):
        super().__init__()

# ?: Custom code delcared here for specific items that instantiate a class, such as trampoline needs to override existing code from the game mode to implement new functionality.
# ?: One way in which this could be done is through decorators, but this will need thorough research in order to implement properly.