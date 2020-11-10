from PyQt5 import QtWidgets as qt
from PyQt5 import QtGui as gui
from PyQt5 import QtCore as core
from functools import partial
from .db import PatientDB
from .case import Case, ViewCase
from .setting import settings
from .my_setup import Setup
from .alert import MsgErrBox
from datetime import date


class MyPatients(qt.QWidget):
    def __init__(self):
        super().__init__()

        # Initialize DB
        self.sqldb = PatientDB()

        # Make UI for MY Patients
        self.BuildUI()

    def BuildUI(self):
        # Vertical Layout
        vbox = qt.QVBoxLayout()

        # Set heading
        heading = qt.QLabel('My Patients')
        heading.setAlignment(core.Qt.AlignCenter)
        heading_font = gui.QFont()
        heading_font.setBold(True)
        heading.setFont(heading_font)

        # Open Patient by ID
        hrow1 = qt.QHBoxLayout()
        self.patientidLE = qt.QLineEdit()
        self.patientidLE.setPlaceholderText('Patient ID')
        self.patientidLE.setValidator(gui.QIntValidator())
        self.patientidLE.textChanged.connect(self.searchPatienById)
        hrow1.addWidget(self.patientidLE)
        hrow1.addStretch()

        # Search Widget
        self.searchpatientLE = qt.QLineEdit()
        self.searchpatientLE.setPlaceholderText('Search Patient')
        self.searchpatientLE.textChanged.connect(self.searchPatients)
        hrow1.addWidget(self.searchpatientLE)

        # Table widget for showing patients List
        self.my_patients_table = qt.QTableWidget()
        self.my_patients_table.setEditTriggers(qt.QTableWidget.NoEditTriggers)

        # Horizontal Box for Bottom button
        hbox = qt.QHBoxLayout()
        new_patient = qt.QPushButton('New Patient')
        refresh = qt.QPushButton('Refresh')
        setup = qt.QPushButton('Setup')

        # Action for Push Button
        new_patient.clicked.connect(self.openNewPatient)
        refresh.clicked.connect(self.getMypatients)
        setup.clicked.connect(self.openSetup)

        hbox.addWidget(refresh)
        hbox.addWidget(setup)
        hbox.addStretch()
        hbox.addWidget(new_patient)

        vbox.addWidget(heading)
        vbox.addLayout(hrow1)
        vbox.addWidget(self.my_patients_table)
        vbox.addLayout(hbox)

        # Set Widget layout
        self.setLayout(vbox)

        # Generate Patients List for first time
        self.getMypatients()

    def openNewPatient(self):
        new_patient = NewPatient()
        new_patient.open()

    def getMypatients(self):
        my_patients = self.sqldb.get_top_20_patients()
        self.make_patient_list(my_patients)

    def searchPatienById(self, pid):
        my_patients = self.sqldb.search_patient_by_id(pid)
        self.make_patient_list(my_patients)

    def searchPatients(self):
        searched_list = self.sqldb.search_patient(self.searchpatientLE.text())
        self.make_patient_list(searched_list)

    def make_patient_list(self, patient_list):
        # Table Setup
        self.my_patients_table.setColumnCount(9)
        self.my_patients_table.setRowCount(
            len(patient_list) if patient_list is not None else 0)
        self.my_patients_table.setHorizontalHeaderLabels(
            ('Patient Id', 'First Name', 'Last Name', 'Age', 'Gender', 'Phone', 'Address', '', ''))
        self.my_patients_table.verticalHeader().setVisible(False)

        # Add items to table
        if patient_list is not None:
            for row, patient in enumerate(patient_list):
                pid, fname, lname, yob, gender, phone, address,  *_ = patient

                # Calculate age
                this_year = date.today().year
                age = this_year - yob

                self.my_patients_table.setItem(
                    row, 0, qt.QTableWidgetItem(str(pid)))
                self.my_patients_table.setItem(
                    row, 1, qt.QTableWidgetItem(str(fname)))
                self.my_patients_table.setItem(
                    row, 2, qt.QTableWidgetItem(str(lname)))
                self.my_patients_table.setItem(
                    row, 3, qt.QTableWidgetItem(str(age)))
                self.my_patients_table.setItem(
                    row, 4, qt.QTableWidgetItem(str(gender)))
                self.my_patients_table.setItem(
                    row, 5, qt.QTableWidgetItem(str(phone)))
                self.my_patients_table.setItem(
                    row, 6, qt.QTableWidgetItem(str(address)))

                # Action Buttons
                edit_case = qt.QPushButton('Edit Case')
                edit_case.clicked.connect(partial(self.edit_case, str(pid)))

                view_case = qt.QPushButton('See Case')
                view_case.clicked.connect(partial(self.view_case, str(pid)))

                # Add row to Table
                self.my_patients_table.setCellWidget(
                    row, 7, view_case
                )
                self.my_patients_table.setCellWidget(
                    row, 8, edit_case
                )

        # Refresh Table
        self.my_patients_table.update()

    def openSetup(self):
        setup = Setup()
        setup.open()

    def edit_case(self, patient_id):
        case = Case()
        case.create_case(patient_id)

    def view_case(self, patient_id):
        patient_case = ViewCase()
        patient_case.view_case(patient_id)


class NewPatient(qt.QDialog):
    def __init__(self):
        super().__init__()

        # Initialize DB
        self.sqldb = PatientDB()

        self.setWindowTitle('New Patient')
        self.set_validations()

    def open(self):
        # Vertical Layout
        formBox = qt.QFormLayout()

        # Patient Name Fields
        self.fnameLE = qt.QLineEdit()
        self.fnameLE.setPlaceholderText('First Name')
        self.fnameLE.setValidator(self.name_validator)
        self.lnameLE = qt.QLineEdit()
        self.lnameLE.setPlaceholderText('Last Name')
        self.lnameLE.setValidator(self.name_validator)
        name_row = qt.QHBoxLayout()
        name_row.addWidget(self.fnameLE)
        name_row.addWidget(self.lnameLE)
        formBox.addRow(qt.QLabel('Patient Name:  '), name_row)

        # Patient Age Field
        self.ageLE = qt.QLineEdit()
        self.ageLE.setPlaceholderText('1 - 150')
        self.ageLE.setValidator(self.age_validator)
        formBox.addRow(qt.QLabel('Age:  '), self.ageLE)

        # Patient gender Field
        self.maleRB = qt.QRadioButton('Male')
        self.maleRB.setChecked(True)
        self.femaleRB = qt.QRadioButton('Female')
        self.othGenRB = qt.QRadioButton('Other')
        sex_grp = qt.QButtonGroup()
        sex_grp.addButton(self.maleRB)
        sex_grp.addButton(self.femaleRB)
        sex_grp.addButton(self.othGenRB)
        gen_row = qt.QHBoxLayout()
        gen_row.addWidget(self.maleRB)
        gen_row.addWidget(self.femaleRB)
        gen_row.addWidget(self.othGenRB)
        formBox.addRow(qt.QLabel('Gender:  '), gen_row)

        # Patient Phone Field
        self.phoneLE = qt.QLineEdit()
        self.phoneLE.setPlaceholderText('Phone / Mobile Number')
        self.phoneLE.setValidator(self.phone_validator)
        formBox.addRow(qt.QLabel('Phone:  '), self.phoneLE)

        # Patient Address Field
        self.addrTE = qt.QTextEdit()
        self.addrTE.setPlaceholderText('Patient Full Address')
        formBox.addRow(qt.QLabel('Address:  '), self.addrTE)

        # Patient Occupation
        self.occLE = qt.QLineEdit()
        self.occLE.setPlaceholderText('Patient Occupation')
        self.occLE.setValidator(self.occupation_validator)
        formBox.addRow(qt.QLabel('Occupation:  '), self.occLE)

        # Patient Marital Status
        self.singleRB = qt.QRadioButton('Single')
        self.singleRB.setChecked(True)
        self.marriedRB = qt.QRadioButton('Married')
        self.unkMarStatRB = qt.QRadioButton('Undisclosed')
        marstat_grp = qt.QButtonGroup()
        marstat_grp.addButton(self.singleRB)
        marstat_grp.addButton(self.marriedRB)
        marstat_grp.addButton(self.unkMarStatRB)
        marstat_row = qt.QHBoxLayout()
        marstat_row.addWidget(self.singleRB)
        marstat_row.addWidget(self.marriedRB)
        marstat_row.addWidget(self.unkMarStatRB)
        formBox.addRow(qt.QLabel('Marital Status:  '), marstat_row)

        # Reference
        self.refLE = qt.QLineEdit()
        self.refLE.setPlaceholderText('Referenced By')
        formBox.addRow(qt.QLabel('Reference:  '), self.refLE)

        # Submit Button
        submit = qt.QPushButton('Submit')
        submit.clicked.connect(self.add_patient)
        right_alignment_row = qt.QHBoxLayout()
        right_alignment_row.addStretch()
        right_alignment_row.addWidget(submit)
        formBox.addRow(qt.QLabel(''), right_alignment_row)

        # Set Widget layout
        self.setLayout(formBox)

        # Show Window
        self.setModal(True)
        self.exec()

    def set_validations(self):
        name_validator_re = core.QRegExp(r'[A-Za-z]+')
        self.name_validator = gui.QRegExpValidator(name_validator_re)

        self.age_validator = gui.QIntValidator(1, 99)

        phone_validator_re = core.QRegExp(r'\+{0,1}[0-9]{10,12}')
        self.phone_validator = gui.QRegExpValidator(phone_validator_re)

        occupation_validator_re = core.QRegExp(r'[A-Za-z][A-Za-z\s]+[A-Za-z]')
        self.occupation_validator = gui.QRegExpValidator(
            occupation_validator_re)

    def add_patient(self):
        # Validation Flag
        valid = 1

        # Get Name
        fname = self.fnameLE.text()
        lname = self.lnameLE.text()
        # Validate name Variables
        if fname == '' and valid == 1:
            MsgErrBox('First Name cannot be empty')
            valid = 0
        elif lname == '' and valid == 1:
            MsgErrBox('Last Name cannot be empty')
            valid = 0

        # Get Age
        age = self.ageLE.text()
        # Validate Age
        if age == '' and valid == 1:
            MsgErrBox('Invalid Age')
        # Calculate Year of birth
        else:
            this_year = date.today().year
            year_of_birth = this_year - int(age)

        # Get gender
        if self.maleRB.isChecked():
            gender = 'M'
        elif self.femaleRB.isChecked():
            gender = 'F'
        else:
            gender = 'O'

        # Get Phone Number
        phone = self.phoneLE.text()

        # Get Address
        address = self.addrTE.toPlainText()

        # Get Occupation
        occupation = self.occLE.text()

        # Get Marital Status
        if self.marriedRB.isChecked():
            marital_status = 'M'
        elif self.singleRB.isChecked():
            marital_status = 'S'
        else:
            marital_status = 'U'

        # Get Reference
        reference = self.refLE.text()

        if valid == 1:
            patient_id = self.sqldb.addPatient(fname, lname, year_of_birth, gender, phone,
                                               address, occupation, marital_status, reference)
            if patient_id is not None:
                case = Case()
                self.close()
                case.create_case(patient_id)
            else:
                MsgErrBox('Unable to create User')
