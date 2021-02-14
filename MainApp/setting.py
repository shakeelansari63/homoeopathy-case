#---------- code:utf8 --------------#
import json
import os
from PyQt5 import QtGui as gui
from PyQt5 import QtCore as core

app_path = os.path.dirname(__file__) + os.path.sep
settings = json.load(open(app_path + "/resources/setting.json"))

# Update absolute path of files
settings["sqlite_db_file"] = app_path + settings["sqlite_db_file"]
settings["icon"] = gui.QIcon(app_path + settings["icon"])
settings["delete_icon"] = app_path + settings["delete_icon"]
settings["boldicon"] = app_path + settings["boldicon"]
settings["italicicon"] = app_path + settings["italicicon"]
settings["underlineicon"] = app_path + settings["underlineicon"]
settings["redicon"] = app_path + settings["redicon"]
settings["blueicon"] = app_path + settings["blueicon"]
settings["greenicon"] = app_path + settings["greenicon"]
settings["whiteicon"] = app_path + settings["whiteicon"]
settings["blackicon"] = app_path + settings["blackicon"]
settings["edit-case"] = app_path + settings["edit-case"]
settings["see-case"] = app_path + settings["see-case"]
settings["save-icon"] = app_path + settings["save-icon"]
settings["add-user"] = app_path + settings["add-user"]
settings["edit-user"] = app_path + settings["edit-user"]
settings["refresh"] = app_path + settings["refresh"]
settings["setup"] = app_path + settings["setup"]
settings["save"] = app_path + settings["save"]
settings["del-user"] = app_path + settings["del-user"]
settings["del-case"] = app_path + settings["del-case"]
settings["db-upgrade"] = app_path + settings["db-upgrade"]
settings["del-set"] = app_path + settings["del-set"]
settings["fontfile"] = app_path + settings["fontfile"]
settings["font"] = gui.QFont()  # 'Noto Sans, Regular', 13, gui.QFont.Bold)
themefile = app_path + settings["themefile"]
with open(themefile, 'r') as fb:
    settings["theme"] = fb.read()
