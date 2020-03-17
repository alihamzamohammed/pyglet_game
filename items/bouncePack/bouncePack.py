from renderer import scroller

def bounce_modifier(func):
    def inner(arg):
        x = scroller
        func(x)
    return inner

    # TODO: CHANGE THIS CODE!