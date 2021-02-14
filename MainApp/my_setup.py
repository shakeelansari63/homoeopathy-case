from PyQt5 import QtWidgets as qt
from PyQt5 import QtGui as gui
from PyQt5 import QtCore as core
from .db import PatientDB, CaseDB, Options
from .alert import MsgSucBox, MsgErrBox
from .setting import settings
from .rich_text import RTextEdit


class Setup(qt.QDialog):
    def __init__(self):
        super().__init__()

        # Database connection
        self.patndb = PatientDB()
        self.casedb = CaseDB()
        self.optdb = Options()

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

        delete_options = qt.QPushButton('Delete All Options')
        delete_options.setIcon(gui.QIcon(settings['del-set']))
        delete_options.setIconSize(core.QSize(28, 28))

        upgrade_db = qt.QPushButton('Upgrade Database')
        upgrade_db.setIcon(gui.QIcon(settings['db-upgrade']))
        upgrade_db.setIconSize(core.QSize(28, 28))

        self.mind_disp_quest = RTextEdit()
        self.mind_disp_quest.setPlaceholderText(
            "Questions for Mind and Disposition")
        self.mind_disp_quest.setText(self.optdb.get_option(settings["MDQ"]))
        update_mind_disp = qt.QPushButton('Update Questions')

        # Acc actions
        delete_patients.clicked.connect(self.del_patn)
        delete_cases.clicked.connect(self.del_case)
        delete_options.clicked.connect(self.del_optns)
        upgrade_db.clicked.connect(self.upgrade_db)
        update_mind_disp.clicked.connect(self.update_mind_disp_ques)

        # Add button to layout
        vbox.addWidget(delete_patients)
        vbox.addWidget(delete_cases)
        vbox.addWidget(delete_options)
        vbox.addWidget(upgrade_db)
        vbox.addWidget(self.mind_disp_quest)
        vbox.addWidget(update_mind_disp)

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

    def del_optns(self):
        self.optdb.reset_all()

        MsgSucBox('All Options Deleted Successfully')

    def update_mind_disp_ques(self):
        key = settings["MDQ"]
        val = self.mind_disp_quest.getText()

        self.optdb.set_option(key, val)

        MsgSucBox('Questions Saved Successfully')
