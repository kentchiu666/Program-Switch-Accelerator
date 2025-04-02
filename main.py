# main.py

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from app.main_window import ProgramSwitchAccelerator
import ctypes
APP_VERSION = "1.0.0"
myappid = f'pythontools.programswitchaccelerator.{APP_VERSION}'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

if __name__ == "__main__":
    app = QApplication(sys.argv)


    icon_path = os.path.join(os.path.dirname(__file__), 'resources', 'app_icon.ico')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    window = ProgramSwitchAccelerator()
    window.show()
    sys.exit(app.exec_())