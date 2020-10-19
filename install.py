import cocos
import pyglet
import easygui
import os
import shutil
import zipfile
from cocos.director import director
import modes
import levels
import items
import cfg
import logger
import message

installTypes = {"mode": modes.GameMode, "itempack": items.ItemPack, "level": levels.Level}

def installer(installType, dialog = "folder"):
    if installType == modes.GameMode:
        typeDict = modes.gamemodes
        typeModule = modes
    elif installType == items.ItemPack:
        typeDict = items.itempacks
        typeModule = items
    elif installType == levels.Level:
        typeDict = levels.levels
        typeModule = levels
    else:
        return False

    if dialog.lower() == "folder":
        installPath = easygui.diropenbox(title="Select expansion pack folder")
    elif dialog.lower() == "file":
        installPath = easygui.fileopenbox(title="Select expansion pack .zip file")
    else:
        return False
    if installPath == "" or installPath == None:
        return False
    
    installPathList = installPath.split("\\")
    
    if installPathList[-1] in list(typeDict.keys()):
        message.showMessage(installPathList[-1] + " is already installed!")
        logger.addLog(installPathList[-1] + " is already installed!", logger.loglevel["info"])
        return False
    else:
        message.showMessage("Installing " + installType.modeType + installPathList[-1])
        try:
            if os.path.isdir(installPath):
                shutil.copytree(installPath, os.getcwd() + typeModule.folder + installPathList[-1])
            else:
                if installPath.lower().endswith(".zip"):
                    with zipfile.ZipFile(installPath, "r") as zip_ref:
                        zip_ref.extractall(os.getcwd() + typeModule.folder + installPathList[-1][:-4])
                else:
                    message.showMessage("The chosen extension is not a folder or zip file.")
                    logger.addLog(installPathList[-1] + " is not a valid folder or .zip file, cannot be installed!", logger.loglevel["warning"])
                    return False
            message.showMessage("Installed " + installType.modeType  + " " + installPathList[-1] + ". Please restart the game to use the new content.")
            logger.addLog(installType.modeType + " " + installPathList[-1] + " installed!", logger.loglevel["debug"])
            return True
        except Exception as e:
            message.showMessage("An error occured installing " + installType.modeType  + " " + installPathList[-1])
            logger.addLog("An error occured installing " + installType.modeType + " " + installPathList[-1], logger.loglevel["warning"])
            logger.addLog("Error installing " + installType.modeType + " " + installPathList[-1] + "\nException:\n" + str(e), logger.loglevel["debug"])
            return False