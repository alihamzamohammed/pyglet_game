import cfg
import os
import datetime

logpath = ""
loglevel = {"error": 0, "warning": 1, "info": 2}

def addLog(message, level = loglevel["info"], first = False):
    if level == loglevel["error"]:
        message = "ERROR: " + message
    elif level == loglevel["warning"]:
        message = "WARNING: " + message
    elif level == loglevel["info"]:
        message = "INFO: " + message
    if first == True:
        message = "\n" + message
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
    addLog("New execution, at: " + str(datetime.datetime.now()) + "\n", loglevel["info"], True)