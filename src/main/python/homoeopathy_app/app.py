#---------- code:utf8 --------------#
from PyQt5 import QtWidgets as qt
from PyQt5 import QtGui as gui
from .setting import settings
from .patients import MyPatients
import sys


class App(qt.QWidget):
    def __init__(self):
        # Create App-
        self.app = qt.QApplication(sys.argv)

        # Initialize super class which is widget
        super().__init__()

    def run(self):

        self.setWindowIcon(gui.QIcon(settings["icon"]))

        # Set Title
        self.setWindowTitle(settings["owner"])

        # Set Position
        self.setGeometry(100, 100, 1200, 800)

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
