#---------- code:utf8 --------------#
import json
import os

app_path = os.path.dirname(__file__) + os.path.sep
settings = json.load(open(app_path + "/setting.json"))

# Update absolute path of files
settings["sqlite_db_file"] = app_path + settings["sqlite_db_file"]
settings["icon"] = app_path + settings["icon"]
settings["delete_icon"] = app_path + settings["delete_icon"]
