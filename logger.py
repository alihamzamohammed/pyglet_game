import cfg
import os

logpath = ""
loglevel = {"error": 0, "warning": 1, "info": 2}

def addLog(message, level = loglevel["info"]):
    if level == loglevel["error"]:
        message = "ERROR: " + message
    elif level == loglevel["warning"]:
        message = "WARNING: " + message
    elif level == loglevel["info"]:
        message = "INFO: " + message
    print(message)
    if not logpath == "":
            log = open(logpath, "a+")
            log.write(message)
            log.close()

def init():
    global logpath
    global loglevel
    if cfg.configuration["Core"]["log"] == "True":
        logpath = cfg.configuration["Core"]["loglocation"]
    print(logpath)