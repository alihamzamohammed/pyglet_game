def configRead(configFile):
    import configparser
    from pyglet.window import key
    temp = {}
    conf = configparser.ConfigParser()
    conf.read(configFile)
    for section in conf.sections():
        for option in conf.options(section):
            temp[option] = conf.get(section, option)
        configuration[section] = temp
        temp = {}
    # TODO: Add in dict string conversion to pyglet.window.key
    #for i in range(len(configuration["Controls"])):
    #    configuration["Controls"][i] == keys[i]

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
    #global keys