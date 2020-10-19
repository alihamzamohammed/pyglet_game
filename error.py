import easygui
import sys
import os

def fatalError(exctype, value, tb):
    easygui.msgbox("A fatal error has occured, and the game has crashed. :(\nThe error type was:" + exctype + "\nAn error report will be available at:")
    with open(os.getcwd() + "error.txt", "w+") as file:
        file.write("A fatal error has occured, and the game has crashed. \nThe error message was:" + exctype + "\nAn error report will be available at: " + os.getcwd() + "error.txt\nError details:\n" + value + "\nStacktrace:\n" + tb)
    sys.exit()