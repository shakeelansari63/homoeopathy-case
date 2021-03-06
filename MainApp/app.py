#---------- code:utf8 --------------#
from PyQt5 import QtWidgets as qt
from PyQt5 import QtGui as gui
from PyQt5 import QtCore as core
from .setting import settings
from .patients import MyPatients
from qtmodern import styles as modernstyle
import sys


class App(qt.QWidget):
    def __init__(self):
        # Create App-
        self.app = qt.QApplication(sys.argv)
        gui.QFontDatabase.addApplicationFont(settings["fontfile"])

        # Set HiDPI
        self.app.setAttribute(core.Qt.AA_UseHighDpiPixmaps)

        # Initialize super class which is widget
        super().__init__()

        # Set Modern Style
        modernstyle.dark(self.app)

    def run(self):

        self.setWindowIcon(settings["icon"])

        # Set Title
        self.setWindowTitle(settings["owner"])

        # Set Position
        self.showMaximized()

        # Add MyPatients Widget in
        box = qt.QVBoxLayout()
        box.addWidget(MyPatients())
        self.setLayout(box)

        # Show window
        self.show()

        # Exit if App closed
        sys.exit(self.app.exec_())


if __name__ == '__main__':
    print("This app cannot be run from here. Import the module and then run app.")
