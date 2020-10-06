import cocos
import pyglet
import events
from cocos import actions, layer, scene, text, sprite
from cocos.director import director
import scaling as sc

rx, ry = director.window.width, director.window.height

class testScroller(scene.Scene):
    
    def __init__(self, *children):
        super().__init__(*children)
        parentLayer = ParentLayer()
        self.add(parentLayer)
        

class ParentLayer(layer.Layer):

    def __init__(self):
        super().__init__()
        scrollManager = layer.ScrollingManager()
        scrollLayer = ScrollLayer()
        scrollBar = ScrollBar()
        
        scrollLayer.x = 0
        scrollLayer.y = 0

        scrollBar.x = rx - (scrollBar.width / 2)
        scrollBar.y = ry / 2

        scrollManager.add(scrollLayer)

        self.add(scrollManager)
        self.add(scrollBar)



class ScrollLayer(layer.ScrollableLayer):

    def __init__(self, parallax=1):
        super().__init__(parallax=parallax)


class ScrollBar(layer.Layer):

    is_event_handler = True

    def __init__(self):
        super().__init__()
        self.img = sprite.Sprite("scrollbar.png")
        self.width = self.img.width
        self.height = self.img.height

        self.add(self.img)
        
        self.width_range = [int((self.x) - (self.width / 2)), int((self.x) + (self.width / 2))]
        self.height_range = [int((self.y) - (self.height / 2)), int((self.y) + (self.width / 2))]

        self.schedule_interval(self.setWH, 1)
        self.resume_scheduler()

    def setWH(self, dt):
        x, y = director.window.width, director.window.height
        print(self.img.height, self.y)
        nmin = sc.scale(int((self.x) - (self.img.width / 2)), int((self.y) - (self.img.height / 2)))
        nmax = sc.scale(int((self.x) + (self.img.width / 2)), int((self.y) + (self.img.height / 2)))
        self.width_range = [int(nmin[0]), int(nmax[0])]
        self.height_range = [int(nmin[1]), int(nmax[1])]


    def on_mouse_motion(self, x, y, dx, dy):
        if x in range(self.width_range[0], self.width_range[1]) and y in range(self.height_range[0], self.height_range[1]):
            self.img.image = pyglet.resource.image("scrollbarHovered.png")
        else:
            self.img.image = pyglet.resource.image("scrollbar.png")


    def on_mouse_press(self, x, y, buttons, modifiers):
        if x in range(self.width_range[0], self.width_range[1]) and y in range(self.height_range[0], self.height_range[1]):
            self.img.image = pyglet.resource.image("scrollbarClicked.png")