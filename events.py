import pyglet
import modes, levels

class MainMenuEvents(pyglet.window.EventDispatcher):

    def __init__(self):
        super().__init__()

    def onProgressFinished(self):
        self.dispatch_event("progressFinished")

    def onPlayButtonClick(self):
        self.dispatch_event("playButtonClicked")

    def onMultiplayerButtonClick(self):
        self.dispatch_event("multiplayerButtonClicked")

    def onSettingsButtonClick(self):
        self.dispatch_event("settingsButtonClicked")

    def onQuitButtonClicked(self):
        self.dispatch_event("quitButtonClicked")

    def backToMainMenu(self):
        self.dispatch_event("showMainMenu")
    
    def mainMenuShowing(self):
        self.dispatch_event("mainMenuIsShowing")

MainMenuEvents.register_event_type("progressFinished")
MainMenuEvents.register_event_type("playButtonClicked")
MainMenuEvents.register_event_type("multiplayerButtonClicked")
MainMenuEvents.register_event_type("quitButtonClicked")
MainMenuEvents.register_event_type("settingsButtonClicked")
MainMenuEvents.register_event_type("showMainMenu")
MainMenuEvents.register_event_type("mainMenuIsShowing")

class SettingsEvents(pyglet.window.EventDispatcher):

    def __init__(self):
        super().__init__()

    def onVideoButtonClick(self):
        self.dispatch_event("showVideoScreen")

    def onSoundButtonClick(self):
        self.dispatch_event("showSoundScreen")

    def onExtensionsButtonClick(self):
        self.dispatch_event("showExtensionsScreen")

    def onMiscButtonClick(self):
        self.dispatch_event("showMiscScreen")

    def aboutPopupShow(self):
        self.dispatch_event("showAboutPopup")

    def aboutPopupHide(self):
        self.dispatch_event("hideAboutPopup")    

    def onControlsButtonClick(self):
        self.dispatch_event("controlsButtonClicked")

SettingsEvents.register_event_type("showVideoScreen")
SettingsEvents.register_event_type("showSoundScreen")
SettingsEvents.register_event_type("showExtensionsScreen")
SettingsEvents.register_event_type("showMiscScreen")
SettingsEvents.register_event_type("showAboutPopup")
SettingsEvents.register_event_type("hideAboutPopup")
SettingsEvents.register_event_type("controlsButtonClicked")

class PauseScreenEvents(pyglet.window.EventDispatcher):

    def __init__(self):
        super().__init__()

    def onPauseScreenAppear(self):
        self.dispatch_event("pauseScreenShowing")

    def onPauseScreenDisappear(self):
        self.dispatch_event("pauseScreenNotShowing")

PauseScreenEvents.register_event_type("pauseScreenShowing")
PauseScreenEvents.register_event_type("pauseScreenNotShowing")

class GameMenuEvents(pyglet.window.EventDispatcher):

    def __init__(self):
        super().__init__()

    def showExtendedInfo(self, idx):
        self.dispatch_event("ExtendedInfoShow", idx)
    
    def hideExtendedInfo(self, idx):
        self.dispatch_event("ExtendedInfoHide", idx)

    def chooseGameMode(self, mode):
        if isinstance(mode, modes.GameMode):
            self.dispatch_event("GameModeChosen", mode)

    def chooseLevel(self, level):
        if isinstance(level, levels.Level):
            self.dispatch_event("LevelChosen", level)

    def onPlayButtonClick(self):
        self.dispatch_event("GamePlayButtonClicked")

    def onReplaceGMMenu(self):
        self.dispatch_event("replaceLevelMenu")

    def onChosenBoxClick(self):
        self.dispatch_event("ChosenBoxClicked")

    def onReturnToGMMenu(self):
        self.dispatch_event("ReturnToGMMenu")

    def levelEditor(self, level):
        self.dispatch_event("openLevelEditor", level)

GameMenuEvents.register_event_type("ExtendedInfoShow")
GameMenuEvents.register_event_type("ExtendedInfoHide")
GameMenuEvents.register_event_type("GameModeChosen")
GameMenuEvents.register_event_type("LevelChosen")
GameMenuEvents.register_event_type("GamePlayButtonClicked")
GameMenuEvents.register_event_type("replaceLevelMenu")
GameMenuEvents.register_event_type("ChosenBoxClicked")
GameMenuEvents.register_event_type("ReturnToGMMenu")
GameMenuEvents.register_event_type("openLevelEditor")

class LevelEditorEvents(pyglet.window.EventDispatcher):

    def __init__(self):
        super().__init__()

    def rowUp(self):
        self.dispatch_event("rowNumberUp")

    def rowDown(self):
        self.dispatch_event("rowNumberDown")

    def itemClick(self, itempack, item):
        self.dispatch_event("itemClicked", itempack, item)

    def activeLayerChange(self):
        self.dispatch_event("activeLayerChanged")
    
    def levelSave(self):
        self.dispatch_event("saveLevel")

    def levelDiscard(self):
        self.dispatch_event("discardLevel")

    def leveleditorGoBack(self):
        self.dispatch_event("leveleditorBack")

LevelEditorEvents.register_event_type("rowNumberUp")
LevelEditorEvents.register_event_type("rowNumberDown")
LevelEditorEvents.register_event_type("itemClicked")
LevelEditorEvents.register_event_type("activeLayerChanged")
LevelEditorEvents.register_event_type("saveLevel")
LevelEditorEvents.register_event_type("discardLevel")
LevelEditorEvents.register_event_type("leveleditorBack")

pausescreenevents = PauseScreenEvents()
mainmenuevents = MainMenuEvents()
settingsevents = SettingsEvents()
gamemenuevents = GameMenuEvents()
leveleditorevents = LevelEditorEvents()