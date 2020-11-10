from PyQt5 import QtWidgets as qt
from PyQt5 import QtGui as gui
from PyQt5 import QtCore as core


class MsgErrBox(qt.QMessageBox):
    def __init__(self, text):
        super().__init__()

        self.setWindowTitle('Error')
        self.setBaseSize(core.QSize(400, 200))
        self.setIcon(qt.QMessageBox.Warning)
        self.setText(text)
        self.exec_()


class MsgSucBox(qt.QMessageBox):
    def __init__(self, text):
        super().__init__()

        self.setWindowTitle('Error')
        self.setBaseSize(core.QSize(400, 200))
        self.setIcon(qt.QMessageBox.Information)
        self.setText(text)
        self.exec_()
