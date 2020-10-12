import cocos
import pyglet
import events
from cocos import actions, layer, scene, text, sprite
from cocos.director import director
import scaling as sc
import cfg
import resources
from scroll import *

rx, ry = director.window.width, director.window.height
reswidth, resheight = [int(res) for res in cfg.resolution.split("x")]

class ScrollLayer(layer.ScrollableLayer):

    def __init__(self, x, y, w, h, sb, parallax=1):
        super().__init__(parallax=parallax)
        self.width = w
        self.height = h
        self.x = x
        self.y = y
        self.sb = sb
        

    def calculate(self):
        if self.get_children() == []:
            self.height = 1
        else:
            self.height = abs(min([x.y for x in self.get_children() if not self.get_children() == []])) + (resheight * 0.2) + resheight
        self.parallax = (self.height - resheight) / ((resheight - (resheight * 0.02)) - (self.sb.img.height / 2) - ((self.sb.img.height / 2) + (resheight * 0.02)))
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
        self._visible = show

        self.width_range = [int((self.x) - (self.width / 2)), int((self.x) + (self.width / 2))]
        self.height_range = [int((self.y) - (self.height / 2)), int((self.y) + (self.width / 2))]

        self.schedule(self.setWH)
        self.resume_scheduler()

        self.sx = rx
        self.sy = ry

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
        if self._visible:
            if x in range(self.width_range[0], self.width_range[1]) and y in range(self.height_range[0], self.height_range[1]):
                self.img.image = pyglet.resource.image("scrollbarClicked.png")
                self.active = True
            else:
                self.active = False

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self._visible:
            if self.active:
                if dy > 0:
                    if (self.y + (resheight * 0.02)) < (resheight - (self.img.height / 2)):
                        self.y += dy
                        self.scrollManager.set_focus(reswidth / 2, self.scrollManager.fy + dy)
                elif dy < 0:
                    if (self.y - (resheight * 0.02)) > (self.img.height / 2):
                        self.y += dy
                        self.scrollManager.set_focus(reswidth / 2, self.scrollManager.fy + dy)

    @property
    def showing(self):
        return self._visible

    @showing.setter
    def showing(self, value):
        self._visible = value
        if value == False:
            self.do(actions.Hide())
        else:
            self.do(actions.Show())