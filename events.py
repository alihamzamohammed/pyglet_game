import pyglet

class RendererEvents(pyglet.window.EventDispatcher):

    def __init__(self):
        super(RendererEvents, self).__init__()

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

RendererEvents.register_event_type("progressFinished")


rendererevents = RendererEvents()