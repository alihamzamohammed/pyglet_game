import cocos
import pyglet
import os
import importlib
import sys
import logger

class GameMode():

    def __init__(self, modeModule):
        super().__init__()
        if hasattr(modeModule, "name"):
            self.name = modeModule.name
        else:
            self.name = "Game Mode"
        if hasattr(modeModule, "desc"):
            self.desc = modeModule.desc
        elif hasattr(modeModule, "description"):
            self.desc = modeModule.description
        else:
            self.desc = "No Description"
        try:
            self.PlatformerController = modeModule.PlatformerController
        except:
            raise PlatformerControllerNotFound
        self.module = modeModule

class PlatformerControllerNotFound(Exception):
    pass

def init():
    global gamemodes
    gamemodes = {}
    for mode in [f.name for f in os.scandir(os.getcwd() + "\\modes\\")]:
        if "_" not in mode:
            try:
                module = importlib.import_module("modes." + mode)
                gamemodes[mode] = GameMode(module)
            except PlatformerControllerNotFound:
                logger.addLog("PlatformerController does not exist in game mode " + mode + ", game mode will not be loaded!", logger.loglevel["warning"])
                continue
            except ModuleNotFoundError:
                logger.addLog("Game mode " + mode + " is not properly structured, game mode will not be loaded!", logger.loglevel["warning"])
