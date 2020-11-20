from py_compile import compile
from PyInstaller.__main__ import run as pybuild
import os

for pyfile in os.listdir('MainApp/'):
    if pyfile.endswith('.py'):
        print(pyfile)
        compile('MainApp/' + pyfile, 'MainAppC/' + pyfile + 'c')

# For importing qtmodern theme
import qtmodern
qtm_path = os.path.dirname(qtmodern.__file__)

pybuild([
    "main.py",
    "--clean",
    "--onedir",
    "--name=HomoeopathyCase",
    "--add-data=./MainAppC:./MainApp",
    "--add-data=./MainApp/img:./MainApp/img",
    "--add-data=./MainApp/resources:./MainApp/resources",
    "--add-data={}:./qtmodern".format(qtm_path),
    "--windowed",
    "--icon=logo.icon"
])