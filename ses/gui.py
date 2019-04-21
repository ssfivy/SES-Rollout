#!/usr/bin/env python3

# GUI interface to SES-Rollout

import os
import sys

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QFile

if __name__ == "__main__":
    app = QApplication(sys.argv)

    filepath = os.path.dirname(os.path.abspath(__file__)) + '/../qt/ses.ui'
    ui_file = QFile(filepath)
    ui_file.open(QFile.ReadOnly)

    loader = QUiLoader()
    window = loader.load(ui_file)
    ui_file.close()
    window.show()

    sys.exit(app.exec_())
