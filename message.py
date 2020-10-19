import cocos
import pyglet
from cocos import text, layer, actions
from cocos.director import director
import cfg

reswidth, resheight = [int(res) for res in cfg.resolution.split("x")]

class Message(layer.ColorLayer):

    def __init__(self, width=None, height=None):
        super().__init__(100, 100, 100, 100, width=width, height=height)
        self.width = reswidth
        self.height = int(resheight * 0.07)
        self.x = 0
        self.y = resheight
        self.showAction = actions.AccelDeccel(actions.MoveTo((self.x, resheight - self.height), 0.5))
        self.hideAction = actions.AccelDeccel(actions.MoveTo((self.x, resheight), 0.5))

        self.lbl = text.Label("", anchor_x="center", anchor_y="center", font_size=18)
        self.lbl.x = self.width / 2
        self.lbl.y = self.height / 2

        self.active = False

        self.add(self.lbl)
         
    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

def remove():
    director.scene.remove(message)

def init():
    global message
    message = Message()

def showMessage(text, duration = 3.5):
    if not message in director.scene.get_children():
        director.scene.add(message)
    if message.active:
        message.do(message.hideAction)
    message.lbl.element.text = text
    message.do(actions.CallFunc(message.activate) + message.showAction + actions.Delay(duration) + message.hideAction + actions.CallFunc(message.deactivate))# + actions.CallFunc(remove))

