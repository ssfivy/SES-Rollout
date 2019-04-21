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

import announce
import monitor_ses_selenium

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
        # Initialisation stuff
        super(SESRMainWindow, self).__init__()
        filepath = resource_path('qt/ses.ui')
        self.ui = uic.loadUi(filepath)
        self.ui.show()

        # Set up all our application behavior
        self.ui.monitor_start.clicked.connect(self.monitor_start)


    def monitor_start(self):
        print('Starting_program!')

        credentials = {}
        credentials['login'] = self.ui.username.text() or ''
        credentials['pass']  = self.ui.password.text() or ''

        if len(credentials['login']) < 1 or len(credentials['pass']) < 1:
            print("No login credentials set.")
            return

        headless = self.ui.browser_headless.isChecked()

        if self.ui.rb_site_live.isChecked():
            livesite = True
        if self.ui.rb_site_training.isChecked():
            livesite = False

        announce.announceStartup(livesite)
        # This works, but blocks the entire UI thread, so we need a separate worker thread
        #monitor_ses_selenium.monitor_jobs(credentials, livesite, headless)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = SESRMainWindow()

    sys.exit(app.exec_())
