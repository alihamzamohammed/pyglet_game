import pyglet

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

MainMenuEvents.register_event_type("progressFinished")
MainMenuEvents.register_event_type("playButtonClicked")
MainMenuEvents.register_event_type("multiplayerButtonClicked")
MainMenuEvents.register_event_type("quitButtonClicked")
MainMenuEvents.register_event_type("settingsButtonClicked")
MainMenuEvents.register_event_type("showMainMenu")

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
    
    def onResWidthChange(self, value):
        self.dispatch_event("resWidthChanged")
    
    def onResHeightChange(self, value):
        self.dispatch_event("resHeightChanged")
    
SettingsEvents.register_event_type("showVideoScreen")
SettingsEvents.register_event_type("showSoundScreen")
SettingsEvents.register_event_type("showExtensionsScreen")
SettingsEvents.register_event_type("showAboutScreen")
SettingsEvents.register_event_type("resWidthChanged")
SettingsEvents.register_event_type("resHeightChanged")

mainmenuevents = MainMenuEvents()
settingsevents = SettingsEvents()
