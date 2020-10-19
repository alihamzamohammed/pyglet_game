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
    #if installType == modes.GameMode or installType == items.ItemPack or installType == levels.Level:
        
        #if installType == modes.GameMode:\
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
    print(installPathList)
    if installPathList[-1] in list(typeDict.keys()):
        return AlreadyInstalled(installType)
    else:
        message.showMessage("Installing " + installType.modeType + installPathList[-1])
        #try:
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
        message.showMessage("Installed " + installType.modeType + installPathList[-1])
        logger.addLog(installType.modeType + installPathList[-1] + " installed!", logger.addLog["debug"])
        return True
        #except Exception as e:
        #    message.showMessage("An error occured installing " + installType.modeType  + " " + installPathList[-1])
        #    logger.addLog("An error occured installing " + installType.modeType + " " + installPathList[-1], logger.loglevel["warning"])
        #    logger.addLog("Error installing " + installType.modeType + " " + installPathList[-1] + "\nException:\n" + str(e), logger.loglevel["debug"])
        #    return False
    
    #     if installType == items.ItemPack:
    #         installPath.split("\\")[-1]
    #         if installPath.split("\\")[-1] in list(items.itempacks.keys()):
    #             return AlreadyInstalled(installType)
    #         else:
    #             message.showMessage("Installing Item Pack " + installPath.split("\\")[-1])
    #             try:
    #                 shutil.copytree(installPath, os.getcwd() + items.folder + installPath.split("\\")[-1])
    #                 message.showMessage("Installed Item Pack ")# + installPath.split("\\")[-1])
    #                 logger.addLog("Item Pack " + installPath.split("\\")[-1] + " installed!", logger.addLog["debug"])
    #                 return True
    #             except Exception as e:
    #                 message.showMessage("An error occured installing Item Pack " + installPath.split("\\")[-1])
    #                 logger.addLog("An error occured installing Item Pack " + installPath.split("\\")[-1], logger.loglevel["warning"])
    #                 logger.addLog("Error installing item pack " + installPath.split("\\")[-1] + "\nException:\n" + str(e), logger.loglevel["debug"])
    #                 return False
        
    #     if installType == levels.Level:
    #         level = installPath.split("\\")[-1]
    #         if level in list(levels.levels.keys()):
    #             return AlreadyInstalled(installType)
    #         else:
    #             message.showMessage("Installing Level " + level)
    #             print("installing")
    #             try:
    #                 shutil.copytree(installPath, os.getcwd() + levels.folder + level)
    #                 print("copied")
    #                 message.showMessage("Installed Level ")# + level)
    #                 logger.addLog("Level " + level + " installed!", logger.addLog["debug"])
    #                 return True
    #             except Exception as e:
    #                 message.showMessage("An error occured installing Level " + level)
    #                 logger.addLog("An error occured installing Level " + level, logger.loglevel["warning"])
    #                 logger.addLog("Error installing level " + level + "\nException:\n" + str(e), logger.loglevel["debug"])
    #                 return False
    # else:
    #     return InvalidType()


class AlreadyInstalled():

    def __init__(self, installType):
        super().__init__()
        self.alreadyInstalledType = installType

class InvalidType():
    pass

def install(installType):
    pass
