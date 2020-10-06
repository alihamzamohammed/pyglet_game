import cocos
import pyglet
import events
from cocos import actions, layer, scene, text, sprite
import scaling


class testScroller(scene.Scene):
    
    def __init__(self, *children):
        super().__init__(*children)
        


class scrollManager(layer.ScrollingManager):

    def __init__(self, viewport=None, do_not_scale=None):
        super().__init__(viewport=viewport, do_not_scale=do_not_scale)


class scrollParentLayer(layer.ScrollableLayer):

    def __init__(self, parallax=1):
        super().__init__(parallax=parallax)


class ScrollBar(layer.Layer):

    is_event_handler = True

    def __init__(self):
        super().__init__()
        self.img = sprite.Sprite("scrollbar.png")
        self.add(self.img)

    def on_mouse_motion(self, x, y, dx, dy):
        self.img.image = pyglet.resource.image("scrollbarHovered.png")

    def on_mouse_press(self, x, y, buttons, modifiers):
        self.img.image = pyglet.resource.image("scrollbarClicked.png")