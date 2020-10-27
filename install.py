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
    
    if installPath.lower().endswith(".zip"):
        newExtensionName = installPathList[-1][:-4]
        isZip = True
    
    else:
        newExtensionName = installPathList[-1]
        isZip = False

    if newExtensionName in list(typeDict.keys()):
        message.showMessage(newExtensionName + " is already installed!")
        logger.addLog(newExtensionName + " is already installed!", logger.loglevel["info"])
        return False
    
    else:    
        message.showMessage("Installing " + installType.modeType + newExtensionName)
        
        try:
            if os.path.isdir(installPath):
                shutil.copytree(installPath, os.getcwd() + typeModule.folder + newExtensionName)

                while os.path.getsize(os.getcwd() + typeModule.folder + newExtensionName) < os.path.getsize(os.getcwd() + typeModule.folder + newExtensionName):
                    print("copying")
                

            else:
        
                if isZip:
                    with zipfile.ZipFile(installPath, "r") as zip_ref:
                        zip_ref.extractall(os.getcwd() + typeModule.folder + newExtensionName)
        
                else:
                    message.showMessage("The chosen extension is not a folder or zip file.")
                    logger.addLog(newExtensionName + " is not a valid folder or .zip file, cannot be installed!", logger.loglevel["warning"])
                    return False
        
            try:
                if installType == modes.GameMode:
                    modes.gamemodes[newExtensionName] = modes.GameMode(os.getcwd() + typeModule.folder + newExtensionName, newExtensionName)
    
                elif installType == items.ItemPack:
                    items.itempacks[newExtensionName] = items.ItemPack(os.getcwd() + typeModule.folder + newExtensionName, newExtensionName)
    
                elif installType == levels.Level:
                    levels.levels[newExtensionName] = levels.Level(os.getcwd() + typeModule.folder + newExtensionName, newExtensionName)
                corrupt = False
            
            except modes.PlatformerControllerNotFound:
                message.showMessage("Game Mode " + newExtensionName + " is corrupt, and has not been installed.")
                logger.addLog("PlatformerController does not exist in game mode " + newExtensionName + ", game mode will not be loaded!", logger.loglevel["warning"])
                corrupt = True
            
            except ModuleNotFoundError:
                message.showMessage("Game Mode " + newExtensionName + " is corrupt, and has not been installed.")
                logger.addLog("Game mode " + newExtensionName + " is not properly structured, game mode will not be loaded!", logger.loglevel["warning"])
                corrupt = True
            
            except items.ItemPackCorrupt as e:
                message.showMessage("Item Pack " + newExtensionName + " is corrupt, and has not been installed.")
                logger.addLog(e.message, logger.loglevel["warning"])
                corrupt = True
            
            except items.DependencyNotFound as e:
                message.showMessage("Item Pack " + newExtensionName + " is corrupt, and has not been installed.")
                logger.addLog(e.message, logger.loglevel["warning"])
                corrupt = True
            
            except levels.LevelCorrupt as e:
                message.showMessage("Level " + newExtensionName + " is corrupt, and has not been installed.")
                logger.addLog(e.message, logger.loglevel["warning"])
                corrupt = True
            
            except levels.DependencyNotFound as e:
                message.showMessage("Level " + newExtensionName + " is corrupt, and has not been installed.")
                logger.addLog(e.message, logger.loglevel["warning"])
                corrupt = True
            
            except levels.LevelDataCorrupt as e:
                message.showMessage("Level " + newExtensionName + " is corrupt, and has not been installed.")
                logger.addLog(e.message + "\n" + e.origEx, logger.loglevel["warning"])
                corrupt = True
            
            finally:
                if corrupt:
                    #shutil.rmtree(os.getcwd() + typeModule.folder + newExtensionName)
                    return False

            message.showMessage("Installed " + installType.modeType  + " " + newExtensionName + ". Please restart the game to use the new content.")
            logger.addLog(installType.modeType + " " + newExtensionName + " installed!", logger.loglevel["debug"])
            return True
        
        except Exception as e:
            message.showMessage("An error occured installing " + installType.modeType  + " " + newExtensionName)
            logger.addLog("An error occured installing " + installType.modeType + " " + newExtensionName, logger.loglevel["warning"])
            logger.addLog("Error installing " + installType.modeType + " " + newExtensionName + "\nException:\n" + str(e), logger.loglevel["debug"])
            return False