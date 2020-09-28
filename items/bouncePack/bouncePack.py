from renderer import scroller

def bounce_modifier(func):
    #pass
    def bounce():
        print("hello this works!")
        return func
    return bounce

    # TODO: CHANGE THIS CODE!