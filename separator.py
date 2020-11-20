from PyQt5 import QtWidgets as qt
from setting import settings


class QHSeperationLine(qt.QFrame):
    '''
    a horizontal seperation line
    '''

    def __init__(self):
        super().__init__()
        self.setMinimumWidth(1)
        self.setFixedHeight(20)
        self.setFrameShape(qt.QFrame.HLine)
        self.setFrameShadow(qt.QFrame.Sunken)
        self.setSizePolicy(qt.QSizePolicy.Preferred,
                           qt.QSizePolicy.Minimum)
        return

        # Set Stylesheet
        self.setStyleSheet(settings["theme"])
