from py_compile import compile
from PyInstaller.__main__ import run as pybuild
import os
import sys
import shutil
import tarfile
from zipfile import ZipFile, ZIP_DEFLATED

def compile_package(packagename):
    # Cleanup existing build and dist dirs
    if os.path.exists('build/'):
        shutil.rmtree('build/')

    if os.path.exists('dist/'):
        shutil.rmtree('dist/')

    if os.path.exists('__pycache__/'):
        shutil.rmtree('__pycache__/')

    for pyfile in os.listdir('MainApp/'):
        if pyfile.endswith('.py'):
            # print(pyfile)
            compile('MainApp/' + pyfile, 'pycs/' + pyfile + 'c')

    # For importing qtmodern theme
    import qtmodern
    qtm_path = os.path.dirname(qtmodern.__file__)

    # Set Logo File
    platformid = sys.platform
    if platformid == 'linux' or platformid == 'darwin':
        logofile = "logo.svg"
        sep = ':'
    else:
        logofile = "logo.ico"
        sep = ';'

    pybuild([
        "main.py",
        "--clean",
        "--onedir",
        "--name={}".format(packagename),
        "--add-data=./pycs{}./MainApp".format(sep),
        "--add-data=./MainApp/img{}./MainApp/img".format(sep),
        "--add-data=./MainApp/resources{}./MainApp/resources".format(sep),
        "--add-data={}{}./qtmodern".format(qtm_path, sep),
        "--windowed",
        "--icon={}".format(logofile)
    ])

    # Cleanup Temporary Files
    shutil.rmtree('pycs/')

    os.remove('{}.spec'.format(packagename))

    # Package in tar File
    if platformid == 'linux' or platformid == 'darwin':
        target_dir = './dist/{}'.format(packagename)
        with tarfile.open('{}.tar.gz'.format(target_dir), 'w:gz') as tar:
            tar.add(target_dir, arcname=packagename)

    # Package in Zip File
    else:
        with ZipFile('{}.zip'.format(target_dir), 'w', ZIP_DEFLATED) as ziph:
            for root, dirs, files in os.walk(target_dir):
                for file in files:
                    ziph.write(os.path.join(root, file))

if __name__ == '__main__':
    compile_package('HomoeopathyCase')