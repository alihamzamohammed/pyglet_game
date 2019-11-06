import cocos

class Window(cocos.layer.Layer):
    
    def __init__(self):
        super(Window, self).__init__()
        cocos.director.director.init(height=1280, width=720, caption="Hello World!")
        cocos.director.director.run(cocos.scene.Scene(Window()))

window1 = Window()