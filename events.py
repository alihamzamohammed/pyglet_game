import pyglet

class RendererEvents(pyglet.window.EventDispatcher):

    def __init__(self):
        super(RendererEvents, self).__init__()

    @classmethod
    def onProgressFinished(cls):
        print("Event dispatching!")
        cls().dispatch_event("progressFinished")
        print("Event dispatched!")        

RendererEvents.register_event_type("progressFinished")