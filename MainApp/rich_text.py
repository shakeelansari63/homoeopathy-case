from PyQt5 import QtWidgets as qt
from PyQt5 import QtGui as gui
from PyQt5 import QtCore as core
from .setting import settings


class RTextEdit(qt.QWidget):
    def __init__(self):
        # Innitialize Widget
        super().__init__()

        # Set resizable Widget
        self.setStyleSheet('margin: 0px; padding:0px;')

        # Widget Layout
        self.layout = qt.QVBoxLayout()

        # Group Box
        self.grp = qt.QGroupBox()

        # Vertical Box layout
        self.vbox = qt.QVBoxLayout()

        # Button Row
        self.hbox = qt.QHBoxLayout()

        # Editor
        self.editor = qt.QTextEdit()

        # Editor Configuration for Rich Text
        self.editor.setAutoFormatting(qt.QTextEdit.AutoAll)
        self.editor.setAcceptRichText(True)
        self.editor.setMinimumHeight(120)
        self.vbox.addWidget(self.editor)
        self.default_color = self.editor.textColor()

        # Buttons
        self.bold = qt.QPushButton('')

        self.italic = qt.QPushButton('')
        self.underline = qt.QPushButton('')
        self.red = qt.QPushButton('')
        self.blue = qt.QPushButton('')
        self.green = qt.QPushButton('')

        # Button Config
        self.bold.setIcon(gui.QIcon(settings['boldicon']))
        self.bold.setIconSize(core.QSize(14, 14))
        self.bold.resize(self.bold.sizeHint().width(),
                         self.bold.sizeHint().height())
        self.bold.setFlat(True)
        self.italic.setIcon(gui.QIcon(settings['italicicon']))
        self.italic.setIconSize(core.QSize(14, 14))
        self.italic.resize(self.italic.sizeHint().width(),
                           self.italic.sizeHint().height())
        self.italic.setFlat(True)
        self.underline.setIcon(gui.QIcon(settings['underlineicon']))
        self.underline.setIconSize(core.QSize(14, 14))
        self.underline.resize(self.underline.sizeHint().width(),
                              self.underline.sizeHint().height())
        self.underline.setFlat(True)
        self.red.setIcon(gui.QIcon(settings['redicon']))
        self.red.setIconSize(core.QSize(14, 14))
        self.red.resize(self.red.sizeHint().width(),
                        self.red.sizeHint().height())
        self.red.setFlat(True)
        self.blue.setIcon(gui.QIcon(settings['blueicon']))
        self.blue.setIconSize(core.QSize(14, 14))
        self.blue.resize(self.blue.sizeHint().width(),
                         self.blue.sizeHint().height())
        self.blue.setFlat(True)
        self.green.setIcon(gui.QIcon(settings['greenicon']))
        self.green.setIconSize(core.QSize(14, 14))
        self.green.resize(self.green.sizeHint().width(),
                          self.green.sizeHint().height())
        self.green.setFlat(True)

        # Remove Tab focus from Buttons
        self.bold.setFocusPolicy(core.Qt.ClickFocus | core.Qt.NoFocus)
        self.italic.setFocusPolicy(core.Qt.ClickFocus | core.Qt.NoFocus)
        self.underline.setFocusPolicy(core.Qt.ClickFocus | core.Qt.NoFocus)
        self.red.setFocusPolicy(core.Qt.ClickFocus | core.Qt.NoFocus)
        self.blue.setFocusPolicy(core.Qt.ClickFocus | core.Qt.NoFocus)
        self.green.setFocusPolicy(core.Qt.ClickFocus | core.Qt.NoFocus)

        # Button Actions
        self.bold.clicked.connect(self.__bold_text)
        self.italic.clicked.connect(self.__italic_text)
        self.underline.clicked.connect(self.__underline_text)
        self.red.clicked.connect(self.__red_text)
        self.blue.clicked.connect(self.__blue_text)
        self.green.clicked.connect(self.__green_text)

        # dd Buttons to Row
        self.hbox.addWidget(self.bold)
        self.hbox.addWidget(self.italic)
        self.hbox.addWidget(self.underline)
        self.hbox.addWidget(self.red)
        self.hbox.addWidget(self.blue)
        self.hbox.addWidget(self.green)
        self.hbox.addStretch()

        # Add Buttons to layout
        self.vbox.addLayout(self.hbox)

        # set layout of widget
        self.grp.setLayout(self.vbox)
        self.layout.addWidget(self.grp)
        self.setLayout(self.layout)

    def __bold_text(self):
        weight = gui.QFont.Bold if self.editor.fontWeight(
        ) == gui.QFont.Normal else gui.QFont.Normal
        self.editor.setFontWeight(weight)

        # Correct Allignment
        self.__correct_allignment()

    def __italic_text(self):
        self.editor.setFontItalic(not self.editor.fontItalic())

        # Correct Allignment
        self.__correct_allignment()

    def __underline_text(self):
        self.editor.setFontUnderline(not self.editor.fontUnderline())

        # Correct Allignment
        self.__correct_allignment()

    def __red_text(self):
        color = gui.QColor(212, 0, 0)
        self.editor.setTextColor(
            color if self.editor.textColor() != color else self.default_color
        )

        # Correct Allignment
        self.__correct_allignment()

    def __blue_text(self):
        color = gui.QColor(0, 170, 212)
        self.editor.setTextColor(
            color if self.editor.textColor() != color else self.default_color
        )

        # Correct Allignment
        self.__correct_allignment()

    def __green_text(self):
        color = gui.QColor(0, 170, 68)
        self.editor.setTextColor(
            color if self.editor.textColor() != color else self.default_color
        )

        # Correct Allignment
        self.__correct_allignment()

    def __correct_allignment(self):
        self.editor.setAlignment(core.Qt.AlignLeft)

    def getText(self):
        return self.editor.toHtml()

    def setText(self, html_text):
        self.editor.setHtml(html_text)

    def setPlaceholderText(self, text):
        self.editor.setPlaceholderText(text)

    def setTabChangesFocus(self, focus):
        self.editor.setTabChangesFocus(focus)
