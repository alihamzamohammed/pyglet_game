import main
import cocos
from cocos import font

resourcePack = "default" 

def getResourcePack():
    global resourcePack
    resourcePack = main.config["Core"]["defaultresource"]

def resourceLoad():
    if not resourcePack == "":
        fontpath = "resources\\" + resourcePack + "\\fonts\\default.ttf"
        cocos.text.pyglet.font.add_file(font)
    else:
        print("Resource pack error!")


