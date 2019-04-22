#!/usr/bin/env python3

# GUI interface to SES-Rollout
# Helpful references: 
# https://stackoverflow.com/questions/2398800/linking-a-qtdesigner-ui-file-to-python-pyqt
# https://stackoverflow.com/questions/14892713/how-do-you-load-ui-files-onto-python-classes-with-pyside/14894550#14894550
# https://stackoverflow.com/questions/37888581/pyinstaller-ui-files-filenotfounderror-errno-2-no-such-file-or-directory
# https://stackoverflow.com/questions/28655198/best-way-to-display-logs-in-pyqt

import logging
from   logging.handlers import RotatingFileHandler
import os
import sys
import threading

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui, uic

import monitor_ses_selenium
import serialout
import speech

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def wait(self, timeout):
        self._stop_event.wait(timeout)

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

class ConsolePanelHandler(QtCore.QObject, logging.Handler):
    # Only tested to inherit QPlainTextEdit
    new_record = QtCore.pyqtSignal(object)

    def __init__(self, parent):
        super().__init__(parent)
        super(logging.Handler).__init__()
        self.parent = parent

    def emit(self, record):
        #self.parent.appendPlainText(self.format(record))
        msg = self.format(record)
        self.new_record.emit(msg) # <---- emit signal here


class SESRMainWindow(QtWidgets.QMainWindow):
    def __init__(self, serial):
        # Initialisation stuff
        super().__init__()
        filepath = resource_path('qt/ses.ui')
        self.ui = uic.loadUi(filepath)
        self.ui.show()

        # Set up behavior - menu bar
        self.ui.actionExit.triggered.connect(self.exit)

        # Set up behavior - logging window
        self.ui.logview.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.ui.logview.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.ui.logview.setMaximumBlockCount(100)

        # Set up behavior - Start tab
        self.monitor_thread = None
        self.ui.monitor_start.clicked.connect(self.monitor_start)
        self.ui.monitor_stop.clicked.connect(self.monitor_stop)
        # Prefill user/pass from environment variable - useful during development
        self.ui.username.setText(os.environ.get("SES_LOGIN") or '')
        self.ui.password.setText(os.environ.get("SES_PASS") or '')

        # Set up behavior - Speaker tab
        self.ui.speaker_test_say.clicked.connect(self.speaker_say)

        # Set up behavior - Serial tab
        self.serial = serial
        self.ui.serial_rescan.clicked.connect(self.serial_rescan_ports)
        self.serial_rescan_ports()
        self.ui.serial_connect.clicked.connect(self.serial_connect)
        self.ui.serial_apply.clicked.connect(self.serial_send)

        # Set up behavior - About tab
        filepath = resource_path('qt/about.txt')
        with open(filepath, 'r', encoding='utf-8') as fb:
            self.ui.aboutText.setPlainText(fb.read())

    def exit(self):
        '''Quit application gracefully'''
        # Todo: Stop all threads
        QtWidgets.QApplication.quit()

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
        announceInitial = self.ui.jobs_announceInitial.isChecked()

        if self.ui.rb_site_live.isChecked():
            livesite = True
        if self.ui.rb_site_training.isChecked():
            livesite = False

        # Change user interface
        self.ui.username.setDisabled(True)
        self.ui.password.setDisabled(True)
        self.ui.monitor_start.setDisabled(True)
        self.ui.monitor_stop.setDisabled(False)
        self.ui.rb_site_live.setDisabled(True)
        self.ui.rb_site_training.setDisabled(True)
        self.ui.browser_headless.setDisabled(True)
        self.ui.jobs_announceInitial.setDisabled(True)

        # Start monitoring
        # Use separate thread so it does not block the main UI thread
        def monitor_worker():
            # no need to announce startup since we already have working speaker test?
            try:
                monitor_ses_selenium.monitor_jobs(credentials, livesite, headless, announceInitial,
                    wait_f=threading.current_thread().wait,
                    runloop_f=threading.current_thread().stopped,
                    serialout=self.serial)
            except:
                logger.exception('Exception in monitor_worker thread')
            finally:
                self.monitor_stop()
        self.monitor_thread = StoppableThread(target=monitor_worker, daemon=True)
        self.monitor_thread.start()

    def monitor_stop(self):
        logging.info('Stopping monitor!')
        # Change user interface
        self.ui.username.setDisabled(False)
        self.ui.password.setDisabled(False)
        self.ui.monitor_start.setDisabled(False)
        self.ui.monitor_stop.setDisabled(True)
        self.ui.rb_site_live.setDisabled(False)
        self.ui.rb_site_training.setDisabled(False)
        self.ui.browser_headless.setDisabled(False)
        self.ui.jobs_announceInitial.setDisabled(False)
        # Set stop flag
        self.monitor_thread.stop()

    def serial_connect(self):
        self.serial.connect_port(
                self.ui.serial_ports.currentText(),
                self.ui.serial_speed.currentText()
                )

    def serial_rescan_ports(self):
        self.serial.list_ports()
        self.ui.serial_ports.clear()
        print(self.serial.all_ports)
        self.ui.serial_ports.insertItems(0, self.serial.all_ports)

    def serial_send(self):
        self.serial.message = self.ui.serial_msg.text()
        if self.ui.serial_encoding.currentIndex() == 0:
            self.serial.isText = True
        elif self.ui.serial_encoding.currentIndex() == 1:
            self.serial.isText = False
        self.serial.announce()

    def speaker_say(self):
        # Use separate thread so it does not block the main UI thread
        def speaker_worker():
            self.ui.speaker_test_say.setDisabled(True)
            logger.info('Playing speaker test message')
            sentence = self.ui.speaker_test_string.text()
            speech.sayText(sentence)
            self.ui.speaker_test_say.setDisabled(False)
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

    logfilename = 'SESRollout.log'
    rfh = RotatingFileHandler(logfilename, maxBytes=1*1024*1024, backupCount=10, encoding='utf-8', delay=True)
    rfh.setLevel(logging.DEBUG)
    rfh.setFormatter(formatter)
    logger.addHandler(rfh)

    # Set up alert backends
    s = serialout.SerialOut()
    # e = ethernetout.EthernetOut()
    # h = httpout.HttpOut()
    # t = telephoneout.TelephoneOut()

    # set up application
    app = QtWidgets.QApplication(sys.argv)
    window = SESRMainWindow(s)

    # set up logging to application
    consolehandler = ConsolePanelHandler(window.ui.logview)
    consolehandler.setLevel(logging.INFO)
    consolehandler.setFormatter(formatter)
    logger.addHandler(consolehandler)
    consolehandler.new_record.connect(window.ui.logview.appendPlainText) # <---- connect QPlainTextEdit.appendPlainText slot

    logger.info('Logging initialised!')

    try:
        ret = app.exec_()
    except:
        logging.exception('exception in application')
    finally:
        sys.exit(ret)
