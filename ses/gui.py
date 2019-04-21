#!/usr/bin/env python3

# GUI interface to SES-Rollout
# Helpful references: 
# https://stackoverflow.com/questions/2398800/linking-a-qtdesigner-ui-file-to-python-pyqt
# https://stackoverflow.com/questions/14892713/how-do-you-load-ui-files-onto-python-classes-with-pyside/14894550#14894550
# https://stackoverflow.com/questions/37888581/pyinstaller-ui-files-filenotfounderror-errno-2-no-such-file-or-directory

import os
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QFile
from PyQt5 import QtGui, uic


# Define function to import external files when using PyInstaller.
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return os.path.join(base_path, relative_path)

class SESRMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(SESRMainWindow, self).__init__()
        filepath = resource_path('qt/ses.ui')
        uic.loadUi(filepath, self)
        self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = SESRMainWindow()

    sys.exit(app.exec_())
