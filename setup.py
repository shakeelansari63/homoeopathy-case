import sys
from setuptools import setup

install_requires = ['PyQt5', 'qtmodern', 'pyinstaller']

setup(
    # basic package data
    name='Homoeopathy Cases',
    version='0.1',
    author='Shakeel Ansari',
    author_email='shakeel.ansari@gmail.com',
    license='',
    url='https://github.com/shakeelansari63/homoeopathy-case',
    install_requires=install_requires,
)
