import pyglet

class RendererEvents(pyglet.window.EventDispatcher):

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

RendererEvents.register_event_type("progressFinished")
RendererEvents.register_event_type("playButtonClicked")
RendererEvents.register_event_type("multiplayerButtonClicked")
RendererEvents.register_event_type("quitButtonClicked")
RendererEvents.register_event_type("settingsButtonClicked")
RendererEvents.register_event_type("showMainMenu")

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

rendererevents = RendererEvents()
settingsevents = SettingsEvents()
