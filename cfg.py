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

def configWrite(configFile):
    import configparser
    conf = configparser.ConfigParser()
    conf.read_dict(configuration)
    with open(configFile, "w") as file:
        conf.write(file)
    file.close()
        

def init():
    global configuration
    configuration = {}
    