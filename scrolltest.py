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
        scrollLayer = ScrollLayer(0, 0, rx * 0.8, ry * 0.8)
        scrollBar = ScrollBar()
        

        scrollLayer.x = 0
        scrollLayer.y = 0

        scrollBar.x = rx - (scrollBar.width / 2)
        scrollBar.y = ry / 2

        scrollManager.add(scrollLayer)

        self.add(scrollManager)
        self.add(scrollBar)



class ScrollLayer(layer.ScrollableLayer):

    def __init__(self, x, y, w, h, parallax=1):
        super().__init__(parallax=parallax)
        self.width = w
        self.height = h
        self.x = x
        self.y = y
        self.t = sprite.Sprite("smallButton.png")
        self.t.x = self.width / 2
        self.t.y = self.height / 2
        
        self.add(self.t)



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

        #self.active = False

    def setWH(self, dt):
        x, y = director.window.width, director.window.height
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
            self.active = True
        else:
            self.active = False
           
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        print(self.y, dy, y)
        if self.active:
            if dy > 0:
                print("up")
                if self.y < (ry - (self.img.height / 2)):
                    self.y += dy
            elif dy < 0:
                print("down")
                if self.y > (self.img.height / 2):
                    self.y += dy



            #if :
            #    top = True
            #else:
            #    top = False
            #
            #if self.y > (self.img.height / 2):
            #    bottom = True
            #    self.y += dy