from PySide2 import QtWidgets as qt
from PySide2 import QtGui as gui
from PySide2 import QtCore as core
from .setting import settings


class MsgErrBox(qt.QMessageBox):
    def __init__(self, text):
        super().__init__()

        self.setWindowTitle('Error')
        self.setBaseSize(core.QSize(400, 200))
        self.setIcon(qt.QMessageBox.Warning)
        self.setText(text)
        self.setWindowIcon(settings["icon"])
        # Set Stylesheet
        self.setStyleSheet(settings["theme"])

        self.exec_()


class MsgSucBox(qt.QMessageBox):
    def __init__(self, text):
        super().__init__()

        self.setWindowTitle('Success')
        self.setBaseSize(core.QSize(400, 200))
        self.setIcon(qt.QMessageBox.Information)
        self.setText(text)
        self.setWindowIcon(settings["icon"])
        # Set Stylesheet
        self.setStyleSheet(settings["theme"])

        self.exec_()


class MsgCloseConfirm(qt.QMessageBox):
    def __init__(self, yes_act, no_act, cancel_act):
        super().__init__()

        self.setWindowTitle('Confirm')
        self.setBaseSize(core.QSize(400, 200))
        self.setStandardButtons(qt.QMessageBox.Yes |
                                qt.QMessageBox.No | qt.QMessageBox.Cancel)
        self.setIcon(qt.QMessageBox.Question)
        self.setText('Do you want to save before closing?')
        self.setWindowIcon(settings["icon"])
        # Set Stylesheet
        self.setStyleSheet(settings["theme"])

        self.yes_act = yes_act
        self.no_act = no_act
        self.cancel_act = cancel_act

        # Take action as per User decision
        decision = self.exec_()

        if decision == qt.QMessageBox.Yes:
            self.yes_act()
        elif decision == qt.QMessageBox.No:
            self.no_act()
        else:
            self.cancel_act()
