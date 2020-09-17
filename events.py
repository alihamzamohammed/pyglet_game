import pyglet
import modes

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

    def onAboutButtonClick(self):
        self.dispatch_event("showAboutScreen")

SettingsEvents.register_event_type("showVideoScreen")
SettingsEvents.register_event_type("showSoundScreen")
SettingsEvents.register_event_type("showExtensionsScreen")
SettingsEvents.register_event_type("showAboutScreen")

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
            print("Selected Game Mode: " + mode.name)

    def chooseLevel(self, idx):
        self.dispatch_event("LevelChosen", idx)

    def onPlayButtonClick(self):
        self.dispatch_event("PlayButtonClicked")

GameMenuEvents.register_event_type("ExtendedInfoShow")
GameMenuEvents.register_event_type("ExtendedInfoHide")
GameMenuEvents.register_event_type("GameModeChosen")
GameMenuEvents.register_event_type("LevelChosen")
GameMenuEvents.register_event_type("PlayButtonClicked")

pausescreenevents = PauseScreenEvents()
mainmenuevents = MainMenuEvents()
settingsevents = SettingsEvents()
gamemenuevents = GameMenuEvents()