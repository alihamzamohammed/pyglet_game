from pyglet.window import key as k

def controlMapping(configFile):
    global keys
    if type(configFile) is not dict:
        return "Wrong file passed"
    for i in list(configFile["Controls"].keys()):
        if configFile["Controls"][i] in keys:
            configFile["Controls"][i] = keys[i.upper()]
        else:
            print("WARNING: Key " + key + " is not a valid key binding!")
            configFile["Controls"][i] = keys["F20"] 
            # Assigns random key here. This key cannot be pressed under normal circumstances, but means the game does not error out because there is an empty keybind
    return configFile

def configRead(configFile):
    import configparser
    global configuration
    from pyglet.window import key
    temp = {}
    conf = configparser.ConfigParser()
    conf.read(configFile)
    for section in conf.sections():
        for option in conf.options(section):
            temp[option] = conf.get(section, option)
        configuration[section] = temp
        temp = {}
    #print(configuration)
    print(controlMapping(configuration))
    #print(configuration)
    # TODO: Add in dict string conversion to pyglet.window.key

def configWrite(configFile):
    import configparser
    conf = configparser.ConfigParser()
    conf.read_dict(configuration)
    with open(configFile, "w") as file:
        conf.write(file)
    file.close()

def init():
    import pyglet.window.key
    global configuration
    configuration = {}
    # TODO: Add in dict string conversion to pyglet.window.key
    global loadedLevel
    loadedLevel = None
    global keys
    keys = {
        "A": k.A, "AMPERSAND": k.AMPERSAND, "APOSTROPHE": k.APOSTROPHE, "ASCIICIRCUM": k.ASCIICIRCUM, 
        "ASCIITILDE": k.ASCIITILDE, "ASTERISK": k.ASTERISK, "AT": k.AT, "B": k.B, 
        "BACKSLASH": k.BACKSLASH, "BACKSPACE": k.BACKSPACE, "BAR": k.BAR, "BEGIN": k.BEGIN, 
        "BRACELEFT": k.BRACELEFT, "BRACERIGHT": k.BRACERIGHT, "BRACKETLEFT": k.BRACKETLEFT, 
        "BRACKETRIGHT": k.BRACKETRIGHT, "BREAK": k.BREAK, "C": k.C, "CANCEL": k.CANCEL, 
        "CAPSLOCK": k.CAPSLOCK, "CLEAR": k.CLEAR, "COLON": k.COLON, "COMMA": k.COMMA, "D": k.D, 
        "DELETE": k.DELETE, "DOLLAR": k.DOLLAR, "DOUBLEQUOTE": k.DOUBLEQUOTE, "DOWN": k.DOWN, 
        "E": k.E, "END": k.END, "ENTER": k.ENTER, "EQUAL": k.EQUAL, "ESCAPE": k.ESCAPE, 
        "EXCLAMATION": k.EXCLAMATION, "EXECUTE": k.EXECUTE, "F": k.F, "F1": k.F1, "F10": k.F10, 
        "F11": k.F11, "F12": k.F12, "F13": k.F13, "F14": k.F14, "F15": k.F15, "F16": k.F16, 
        "F17": k.F17, "F18": k.F18, "F19": k.F19, "F2": k.F2, "F20": k.F20, "F3": k.F3, "F4": k.F4, 
        "F5": k.F5, "F6": k.F6, "F7": k.F7, "F8": k.F8, "F9": k.F9, "FIND": k.FIND, 
        "FUNCTION": k.FUNCTION, "G": k.G, "GRAVE": k.GRAVE, "GREATER": k.GREATER, "H": k.H, 
        "HASH": k.HASH, "HELP": k.HELP, "HOME": k.HOME, "I": k.I, "INSERT": k.INSERT, "J": k.J, 
        "K": k.K, "L": k.L, "LALT": k.LALT, "LCOMMAND": k.LCOMMAND, "LCTRL": k.LCTRL, "LEFT": k.LEFT, 
        "LESS": k.LESS, "LINEFEED": k.LINEFEED, "LMETA": k.LMETA, "LOPTION": k.LOPTION, 
        "LSHIFT": k.LSHIFT, "LWINDOWS": k.LWINDOWS, "M": k.M, "MENU": k.MENU, "MINUS": k.MINUS, 
        "MODESWITCH": k.MODESWITCH, "MOD_ACCEL": k.MOD_ACCEL, "MOD_ALT": k.MOD_ALT, 
        "MOD_CAPSLOCK": k.MOD_CAPSLOCK, "MOD_COMMAND": k.MOD_COMMAND, "MOD_CTRL": k.MOD_CTRL, 
        "MOD_FUNCTION": k.MOD_FUNCTION, "MOD_NUMLOCK": k.MOD_NUMLOCK, "MOD_OPTION": k.MOD_OPTION, 
        "MOD_SCROLLLOCK": k.MOD_SCROLLLOCK, "MOD_SHIFT": k.MOD_SHIFT, "MOD_WINDOWS": k.MOD_WINDOWS, 
        "MOTION_BACKSPACE": k.MOTION_BACKSPACE, "MOTION_BEGINNING_OF_FILE": k.MOTION_BEGINNING_OF_FILE, 
        "MOTION_BEGINNING_OF_LINE": k.MOTION_BEGINNING_OF_LINE, "MOTION_DELETE": k.MOTION_DELETE, 
        "MOTION_DOWN": k.MOTION_DOWN, "MOTION_END_OF_FILE": k.MOTION_END_OF_FILE, 
        "MOTION_END_OF_LINE": k.MOTION_END_OF_LINE, "MOTION_LEFT": k.MOTION_LEFT, 
        "MOTION_NEXT_PAGE": k.MOTION_NEXT_PAGE, "MOTION_NEXT_WORD": k.MOTION_NEXT_WORD, 
        "MOTION_PREVIOUS_PAGE": k.MOTION_PREVIOUS_PAGE, "MOTION_PREVIOUS_WORD": k.MOTION_PREVIOUS_WORD, 
        "MOTION_RIGHT": k.MOTION_RIGHT, "MOTION_UP": k.MOTION_UP, "N": k.N, "NUMLOCK": k.NUMLOCK, 
        "NUM_0": k.NUM_0, "NUM_1": k.NUM_1, "NUM_2": k.NUM_2, "NUM_3": k.NUM_3, "NUM_4": k.NUM_4, 
        "NUM_5": k.NUM_5, "NUM_6": k.NUM_6, "NUM_7": k.NUM_7, "NUM_8": k.NUM_8, "NUM_9": k.NUM_9, 
        "NUM_ADD": k.NUM_ADD, "NUM_BEGIN": k.NUM_BEGIN, "NUM_DECIMAL": k.NUM_DECIMAL, 
        "NUM_DELETE": k.NUM_DELETE, "NUM_DIVIDE": k.NUM_DIVIDE, "NUM_DOWN": k.NUM_DOWN, 
        "NUM_END": k.NUM_END, "NUM_ENTER": k.NUM_ENTER, "NUM_EQUAL": k.NUM_EQUAL, "NUM_F1": k.NUM_F1, 
        "NUM_F2": k.NUM_F2, "NUM_F3": k.NUM_F3, "NUM_F4": k.NUM_F4, "NUM_HOME": k.NUM_HOME, 
        "NUM_INSERT": k.NUM_INSERT, "NUM_LEFT": k.NUM_LEFT, "NUM_MULTIPLY": k.NUM_MULTIPLY, 
        "NUM_NEXT": k.NUM_NEXT, "NUM_PAGE_DOWN": k.NUM_PAGE_DOWN, "NUM_PAGE_UP": k.NUM_PAGE_UP, 
        "NUM_PRIOR": k.NUM_PRIOR, "NUM_RIGHT": k.NUM_RIGHT, "NUM_SEPARATOR": k.NUM_SEPARATOR, 
        "NUM_SPACE": k.NUM_SPACE, "NUM_SUBTRACT": k.NUM_SUBTRACT, "NUM_TAB": k.NUM_TAB, 
        "NUM_UP": k.NUM_UP, "O": k.O, "P": k.P, "PAGEDOWN": k.PAGEDOWN, "PAGEUP": k.PAGEUP, 
        "PARENLEFT": k.PARENLEFT, "PARENRIGHT": k.PARENRIGHT, "PAUSE": k.PAUSE, "PERCENT": k.PERCENT, 
        "PERIOD": k.PERIOD, "PLUS": k.PLUS, "POUND": k.POUND, "PRINT": k.PRINT, "Q": k.Q, 
        "QUESTION": k.QUESTION, "QUOTELEFT": k.QUOTELEFT, "R": k.R, "RALT": k.RALT, "RCOMMAND": k.RCOMMAND, 
        "RCTRL": k.RCTRL, "REDO": k.REDO, "RETURN": k.RETURN, "RIGHT": k.RIGHT, "RMETA": k.RMETA, 
        "ROPTION": k.ROPTION, "RSHIFT": k.RSHIFT, "RWINDOWS": k.RWINDOWS, "S": k.S, 
        "SCRIPTSWITCH": k.SCRIPTSWITCH, "SCROLLLOCK": k.SCROLLLOCK, "SELECT": k.SELECT, 
        "SEMICOLON": k.SEMICOLON, "SLASH": k.SLASH, "SPACE": k.SPACE, "SYSREQ": k.SYSREQ, "T": k.T, 
        "TAB": k.TAB, "U": k.U, "UNDERSCORE": k.UNDERSCORE, "UNDO": k.UNDO, "UP": k.UP, "V": k.V, "W": k.W, 
        "X": k.X, "Y": k.Y, "Z": k.Z, "_0": k._0, "_1": k._1, "_2": k._2, "_3": k._3, "_4": k._4, "_5": k._5, 
        "_6": k._6, "_7": k._7, "_8": k._8, "_9": k._9}