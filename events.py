import pyglet

class RendererEvents(pyglet.window.EventDispatcher):

    def __init__(self):
        super(RendererEvents, self).__init__()

    def onProgressFinished(self):
        print("Event dispatching!")
        self.dispatch_event("progressFinished")
        print("Event dispatched!")        

RendererEvents.register_event_type("progressFinished")


rendererevents = RendererEvents()