from MainApp import App
from PyQt5 import QtWidgets as qt, QtCore as core, QtGui as gui
from MainApp.RichTextEditor import RTextEdit
from functools import partial
#from MainApp.case import Case

app = App()
# app.run()

#test = Case()
# test.casedb.reset_all()
# test.create_case(1)


win = qt.QDialog()
vlay = qt.QVBoxLayout()

edit = RTextEdit()
vlay.addWidget(edit)

win.setLayout(vlay)

win.show()
app.run()


# def update_format():
#    pass
