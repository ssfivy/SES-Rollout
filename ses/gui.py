#!/usr/bin/env python3

# GUI interface to SES-Rollout
# Helpful references: 
# https://stackoverflow.com/questions/2398800/linking-a-qtdesigner-ui-file-to-python-pyqt
# https://stackoverflow.com/questions/14892713/how-do-you-load-ui-files-onto-python-classes-with-pyside/14894550#14894550
# https://stackoverflow.com/questions/37888581/pyinstaller-ui-files-filenotfounderror-errno-2-no-such-file-or-directory

import logging
import os
import sys
import threading
import multiprocessing

from PyQt5 import QtWidgets
from PyQt5.QtCore import QFile
from PyQt5 import QtGui, uic

import announce
import monitor_ses_selenium
import speech

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

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
        super().__init__()
        filepath = resource_path('qt/ses.ui')
        self.ui = uic.loadUi(filepath)
        self.ui.show()

        # Set up behavior - Start tab
        self.monitor_thread = None
        self.ui.monitor_start.clicked.connect(self.monitor_start)
        self.ui.monitor_stop.clicked.connect(self.monitor_stop)

        # Set up behavior - Speaker tab
        self.ui.speaker_test_say.clicked.connect(self.speaker_say)

        # Set up behavior - Serial tab

        # Set up behavior - About tab


    def monitor_start(self):
        logging.info('Starting monitor!')

        # Grab all information needed to start
        credentials = {}
        credentials['login'] = self.ui.username.text() or ''
        credentials['pass']  = self.ui.password.text() or ''

        if len(credentials['login']) < 1 or len(credentials['pass']) < 1:
            logging.error("No login credentials set.")
            return

        headless = self.ui.browser_headless.isChecked()

        if self.ui.rb_site_live.isChecked():
            livesite = True
        if self.ui.rb_site_training.isChecked():
            livesite = False

        # Change user interface
        self.ui.username.setDisabled(True)
        self.ui.password.setDisabled(True)
        self.ui.monitor_start.setDisabled(True)
        self.ui.monitor_stop.setDisabled(False)

        # Start monitoring
        # Use separate thread so it does not block the main UI thread
        def monitor_worker():
            # no need to announce startup since we already have working speaker test?
            monitor_ses_selenium.monitor_jobs(credentials, livesite, headless)
        self.monitor_thread = multiprocessing.Process(target=monitor_worker)
        self.monitor_thread.start()

    def monitor_stop(self):
        logging.info('Stopping monitor!')
        # Change user interface
        self.ui.username.setDisabled(False)
        self.ui.password.setDisabled(False)
        self.ui.monitor_start.setDisabled(False)
        self.ui.monitor_stop.setDisabled(True)
        # Set stop flag
        self.monitor_thread.terminate()

    def speaker_say(self):
        # Use separate thread so it does not block the main UI thread
        def speaker_worker():
            sentence = self.ui.speaker_test_string.text()
            speech.sayText(sentence)
        t = threading.Thread(target=speaker_worker)
        t.start()

if __name__ == "__main__":
    # set up logging
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s : %(message)s')

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.info('Logging initialised!')

    # set up application
    app = QtWidgets.QApplication(sys.argv)
    window = SESRMainWindow()

    sys.exit(app.exec_())
