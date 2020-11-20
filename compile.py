from py_compile import compile
from PyInstaller.__main__ import run as pybuild
import os
import sys
import shutil

# Cleanup existing build and dist dirs
if os.path.exists('build/'):
    shutil.rmtree('build/')

if os.path.exists('dist/'):
    shutil.rmtree('dist/')

if os.path.exists('__pycache__/'):
    shutil.rmtree('__pycache__/')

for pyfile in os.listdir('MainApp/'):
    if pyfile.endswith('.py'):
        print(pyfile)
        compile('MainApp/' + pyfile, 'pycs/' + pyfile + 'c')

# For importing qtmodern theme
import qtmodern
qtm_path = os.path.dirname(qtmodern.__file__)

# Set Logo File
if sys.platform == 'linux' or sys.platform == 'darwin':
    logofile = "logo.svg"
else:
    logofile = "logo.ico"

pybuild([
    "main.py",
    "--clean",
    "--onedir",
    "--name=HomoeopathyCase",
    "--add-data=./pycs:./MainApp",
    "--add-data=./MainApp/img:./MainApp/img",
    "--add-data=./MainApp/resources:./MainApp/resources",
    "--add-data={}:./qtmodern".format(qtm_path),
    "--windowed",
    "--icon={}".format(logofile)
])

# Cleanup Temporary Files
shutil.rmtree('pycs/')