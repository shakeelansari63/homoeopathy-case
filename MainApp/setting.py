#---------- code:utf8 --------------#
import json
import os
from PyQt5 import QtGui as gui
from PyQt5 import QtCore as core

app_path = os.path.dirname(__file__) + os.path.sep
settings = json.load(open(app_path + "/setting.json"))

# Update absolute path of files
settings["sqlite_db_file"] = app_path + settings["sqlite_db_file"]
settings["icon"] = gui.QIcon(app_path + settings["icon"])
settings["delete_icon"] = app_path + settings["delete_icon"]
settings["fontfile"] = app_path + settings["fontfile"]
settings["font"] = gui.QFont()  # 'Noto Sans, Regular', 13, gui.QFont.Bold)
themefile = app_path + settings["themefile"]
with open(themefile, 'r') as fb:
    settings["theme"] = fb.read()

