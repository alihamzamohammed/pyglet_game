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
    with open(configFile, "r+") as file:
        print(configuration)
        conf.write(file)
        print(file.read())
    file.close()

def init():
    global configuration
    configuration = {}
    