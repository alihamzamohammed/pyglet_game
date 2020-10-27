import easygui
import sys
import os
import traceback

def fatalError(exctype, value, tb):
    easygui.msgbox("A fatal error has occured, and the game has crashed. :(\nThe error type was: " + repr(exctype) + "\nAn error report will be available at: " + os.getcwd() + "\\error.txt")
    with open(os.getcwd() + "\\error.txt", "w+") as file:
        file.write("A fatal error has occured, and the game has crashed.\n\nERROR REPORT: \nThe error message was: " + repr(exctype) + "\nError details:\n" + repr(value) + "\nStacktrace:\n" + "".join(x for x in traceback.format_exception(exctype, value, tb)))
    sys.exit()