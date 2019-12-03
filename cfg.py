def configRead(configFile):
    import configparser
    temp = {}
    conf = configparser.ConfigParser()
    conf.read(configFile)
    for section in conf.sections():
        for option in conf.options(section):
            temp[option] = conf.get(section, option)
        configuration[section] = temp
        temp = {}


def init():
    global configuration
    configuration = {}
    