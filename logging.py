import main
import os

logpath = ""
info = 2
warning = 1
error = 0

def log(message, level = info):
    if level == error:
        message = "ERROR: " + message
        print(message)
        if not logpath == "":
            log = open(logpath, "a+")
            log.write(message)
            log.close()

def main():
    if main.config["Core"]["Log"] == True:
        logpath = main.config["Core"]["LogLocation"]