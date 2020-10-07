import cocos
import pyglet
import events
from cocos import actions, layer, scene, text, sprite
from cocos.director import director
import scaling as sc
import cfg
import resources

rx, ry = director.window.width, director.window.height
reswidth, resheight = [int(res) for res in cfg.resolution.split("x")]

class testScroller(scene.Scene):
    
    def __init__(self, *children):
        super().__init__(*children)
        parentLayer = ParentLayer()
        self.add(parentLayer)
        

class ParentLayer(layer.Layer):

    def __init__(self):
        super().__init__()
        scrollManager = layer.ScrollingManager()
        scrollLayer = ScrollLayer(reswidth/2, resheight, reswidth, 1440)#((resheight * 0.5) / resheight))
        scrollBar = ScrollBar(scrollManager)
        
        scrollLayer.x = 0
        scrollLayer.y = 0

        scrollBar.x = reswidth - (scrollBar.width / 2)
        scrollBar.y = (resheight - (resheight * 0.02)) - (scrollBar.img.height / 2)

        scrollManager.add(scrollLayer)
        scrollManager.set_focus(reswidth / 2, resheight / 2)

        self.add(scrollManager)
        self.add(scrollBar)


class ScrollLayer(layer.ScrollableLayer):

    def __init__(self, x, y, w, h, parallax=1):
        super().__init__(parallax=parallax)
        self.width = w
        self.height = h
        self.x = x
        self.y = y
        
        #self.t = sprite.Sprite("smallButton.png")
        #self.t.x = 0
        #self.t.y = 0
        
        #self.add(self.t)
        

        self.title = text.Label("Controls", font_name=resources.font[1], font_size=50, anchor_y="top", anchor_x="center")
        self.title.x = reswidth / 2
        self.title.y = resheight * 0.85 
        self.add(self.title)
        self.obj = []
        #for i in range(-1, 20):
        #    sp = sprite.Sprite("smallButton.png")
        #    if i == -1 or i == 19:
        #        sp.image = pyglet.resource.image("smallButtonHovered.png")
        #    sp.x = reswidth / 2
        #    sp.y = (resheight * 0.5) * -i
        #    print(sp.y)
        #    self.obj.append(sp)
        #    self.add(sp)
        sp = sprite.Sprite("smallButtn.png")
        sp.x = reswidth / 2
        sp.height = -720
        self.add(sp)

        #self.height = resheight - (self.obj[-1].y - (resheight * 0.4))
        #self.height = 1440
        self.parallax = (self.height / resheight)# + 1.5
        #self.parallax = 6
        print(self.height, self.parallax)
        self.set_view(self.x, self.y, self.width, self.height)


    def set_view(self, x, y, w, h, viewport_ox=0, viewport_oy=0):
        """Sets the position of the viewport for this layer.

        Arguments:
            x (float): The view x position
            y (float): The view y position
            w (float): The width of the view
            h (float): The height of the view
            viewport_ox (float) : The viewport x origin
            viewport_oy (float) : The viewport y origin
        """
        #x *= self.parallax
        y *= self.parallax
        self.view_x, self.view_y = x, y
        self.view_w, self.view_h = w, h
        x -= self.origin_x
        y -= self.origin_y
        x -= viewport_ox
        y -= viewport_oy
        self.position = (-x, -y)


class ScrollBar(layer.Layer):

    is_event_handler = True

    def __init__(self, scrollManager, show = True):
        super().__init__()
        self.img = sprite.Sprite("scrollbar.png")
        self.width = self.img.width
        self.height = self.img.height
        self.scrollManager = scrollManager

        self.add(self.img)
        
        if not show:
            self.do(actions.Hide())

        self.width_range = [int((self.x) - (self.width / 2)), int((self.x) + (self.width / 2))]
        self.height_range = [int((self.y) - (self.height / 2)), int((self.y) + (self.width / 2))]

        self.schedule_interval(self.setWH, 1)
        self.resume_scheduler()

        self.sx = rx
        self.sy = ry

        #self.active = False

    def setWH(self, dt):
        x, y = director.window.width, director.window.height
        nmin = sc.scale(int((self.x) - (self.img.width / 2)), int((self.y) - (self.img.height / 2)))
        nmax = sc.scale(int((self.x) + (self.img.width / 2)), int((self.y) + (self.img.height / 2)))
        self.sx, self.sy = sc.scale(rx, ry)
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
        if self.active:
            if dy > 0:
                if (self.y + (self.sy * 0.02)) < (ry - (self.img.height / 2)):
                    self.y += dy
                    self.scrollManager.set_focus(reswidth / 2, self.scrollManager.fy + dy)
            elif dy < 0:
                if (self.y - (self.sy * 0.02)) > (self.img.height / 2):
                    self.y += dy
                    self.scrollManager.set_focus(reswidth / 2, self.scrollManager.fy + dy)
