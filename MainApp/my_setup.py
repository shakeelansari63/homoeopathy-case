from PyQt5 import QtWidgets as qt
from PyQt5 import QtGui as gui
from PyQt5 import QtCore as core
from .db import PatientDB, CaseDB
from .alert import MsgSucBox, MsgErrBox
from .setting import settings


class Setup(qt.QDialog):
    def __init__(self):
        super().__init__()

        # Database connection
        self.patndb = PatientDB()
        self.casedb = CaseDB()

        # Set Stylesheet
        self.setStyleSheet(settings["theme"])

    def open(self):
        vbox = qt.QVBoxLayout()

        # Create Buttons
        delete_patients = qt.QPushButton('Delete All Patients')
        delete_patients.setIcon(gui.QIcon(settings['del-user']))
        delete_patients.setIconSize(core.QSize(28, 28))

        delete_cases = qt.QPushButton('Delete All Cases')
        delete_cases.setIcon(gui.QIcon(settings['del-case']))
        delete_cases.setIconSize(core.QSize(28, 28))

        upgrade_db = qt.QPushButton('Upgrade Database')
        upgrade_db.setIcon(gui.QIcon(settings['db-upgrade']))
        upgrade_db.setIconSize(core.QSize(28, 28))

        # Acc actions
        delete_patients.clicked.connect(self.del_patn)
        delete_cases.clicked.connect(self.del_case)
        upgrade_db.clicked.connect(self.upgrade_db)

        # Add button to layout
        vbox.addWidget(delete_patients)
        vbox.addWidget(delete_cases)
        vbox.addWidget(upgrade_db)

        # Set window layout
        self.setLayout(vbox)

        self.setWindowTitle('Setup')
        self.setModal(True)
        self.setFont(settings["font"])
        self.setWindowIcon(settings["icon"])
        self.exec()

    def del_patn(self):
        self.patndb.reset_all()
        max_patn_id = self.patndb.get_max_patients()
        if max_patn_id == 0:
            MsgSucBox('Patients Deleted Successfully')
        else:
            MsgErrBox('Unable to Delete Patients')

    def del_case(self):
        self.casedb.reset_all()
        max_case_id = self.casedb.get_max_caseid()
        if max_case_id == 0:
            MsgSucBox('Cases Deleted Successfully')
        else:
            MsgSucBox('Unable to Delete Cases')

    def upgrade_db(self):
        retcode = self.casedb.upgrade_db()

        if retcode == 0:
            MsgSucBox('Database Upgraded Successfully')
        else:
            MsgSucBox('Database already up to date')
