import cocos
import pyglet
import os
import importlib
import sys

def init():
    global gamemodes
    gamemodes = {}
    for mode in [f.name for f in os.scandir(os.getcwd() + "\\modes\\")]:
        if "_" not in mode:
            module = importlib.import_module("modes.freeplay")# + mode)
            gamemodes[mode] = module.main()
    print(gamemodes)