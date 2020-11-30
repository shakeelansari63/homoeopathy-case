from PyQt5 import QtWidgets as qt
from PyQt5 import QtGui as gui
from PyQt5 import QtCore as core
from .db import PatientDB, CaseDB
from .alert import MsgErrBox, MsgSucBox, MsgCloseConfirm
from .setting import settings
from .separator import QHSeperationLine
from datetime import date
from functools import partial
from .rich_text import RTextEdit


class Case(qt.QDialog):
    """ Create New case """

    def __init__(self):
        super().__init__()

        # Db Connection
        self.sqldb = PatientDB()
        self.casedb = CaseDB()

        # Set Stylesheet
        self.setStyleSheet(settings["theme"])

        # Variable to check if case is saved
        self.case_saved = False

    def create_case(self, patient_id=None):
        self.pid = patient_id

        # Get user detail from Database
        _, fname, lname, yob, gender, *_ = self.sqldb.\
            get_patient_by_id(self.pid)
        # Calculate Age
        this_year = date.today().year
        age = this_year - yob

        # Srollable Ares
        outer_box = qt.QVBoxLayout()
        scroll_widget = qt.QWidget()
        scroll_win = qt.QScrollArea()
        scroll_win.setVerticalScrollBarPolicy(core.Qt.ScrollBarAlwaysOn)
        scroll_win.setHorizontalScrollBarPolicy(core.Qt.ScrollBarAlwaysOff)
        scroll_win.setWidgetResizable(True)

        self.vbox = qt.QVBoxLayout()

        # Group of Chief Complaint
        chief_complaint_grp = qt.QGroupBox('Chief Complaint')
        ccgrp = qt.QVBoxLayout()
        ccform = qt.QHBoxLayout()
        # Complaint Location
        self.cc_location = RTextEdit()
        self.cc_location.setPlaceholderText('Location')
        self.cc_location.setTabChangesFocus(True)
        cc_loc_col = qt.QVBoxLayout()
        cc_loc_col.addWidget(qt.QLabel('Location'))
        cc_loc_col.addWidget(self.cc_location)
        cc_loc_col.setAlignment(core.Qt.AlignTop)
        ccform.addLayout(cc_loc_col)
        # Complaint Sensation
        self.cc_sensation = RTextEdit()
        self.cc_sensation.setPlaceholderText('Sensation')
        self.cc_sensation.setTabChangesFocus(True)
        cc_sen_col = qt.QVBoxLayout()
        cc_sen_col.addWidget(qt.QLabel('Sensation'))
        cc_sen_col.addWidget(self.cc_sensation)
        cc_sen_col.setAlignment(core.Qt.AlignTop)
        ccform.addLayout(cc_sen_col)
        # Modality
        self.cc_amelioration = RTextEdit()
        self.cc_amelioration.setPlaceholderText('Amelioration')
        self.cc_amelioration.setTabChangesFocus(True)
        self.cc_aggravation = RTextEdit()
        self.cc_aggravation.setPlaceholderText('Aggravation')
        self.cc_aggravation.setTabChangesFocus(True)
        cc_mod_col = qt.QVBoxLayout()
        cc_mod_col.addWidget(qt.QLabel('Modality'))
        cc_mod_col.addWidget(self.cc_aggravation)
        cc_mod_col.addWidget(self.cc_amelioration)
        cc_mod_col.setAlignment(core.Qt.AlignTop)
        ccform.addLayout(cc_mod_col)
        # Concometent
        self.cc_concometent = RTextEdit()
        self.cc_concometent.setPlaceholderText('Concomitant')
        self.cc_concometent.setTabChangesFocus(True)
        cc_conc_col = qt.QVBoxLayout()
        cc_conc_col.addWidget(qt.QLabel('Concomitant'))
        cc_conc_col.addWidget(self.cc_concometent)
        cc_conc_col.setAlignment(core.Qt.AlignTop)
        ccform.addLayout(cc_conc_col)
        # Add form to Group
        ccgrp.addLayout(ccform)
        # Add Allopathy Medicine
        cc_allop_row = qt.QFormLayout()
        self.cc_allopathymed = RTextEdit()
        self.cc_allopathymed.setPlaceholderText('Allopathy Medicine')
        self.cc_allopathymed.setTabChangesFocus(True)
        cc_allop_row.addRow(
            qt.QLabel('Allopathy Medicine:  '),
            self.cc_allopathymed
        )
        ccgrp.addLayout(cc_allop_row)
        # Set group
        chief_complaint_grp.setLayout(ccgrp)
        # Add Group to Vbox
        self.vbox.addWidget(chief_complaint_grp)

        # Associated Complaint
        self.associated_complaint_list = {}
        self.associated_complaint_widgets = {}
        asso_complaint_grp = qt.QGroupBox('Associated Complaint')
        self.assocVbox = qt.QVBoxLayout()
        # Add Associated Group
        asso_complaint_grp.setLayout(self.assocVbox)
        # Add to VBox
        self.vbox.addWidget(asso_complaint_grp)

        # Button to add new
        add_assoc_btn = qt.QPushButton('Add Associated Complaint')
        add_assoc_btn.clicked.connect(self.add_associated_complaint)
        btnrow = qt.QHBoxLayout()
        btnrow.addStretch()
        btnrow.addWidget(add_assoc_btn)
        self.vbox.addLayout(btnrow)

        # Past History
        past_history_grp = qt.QGroupBox('Past History')
        phvbox = qt.QVBoxLayout()
        self.past_hist = RTextEdit()
        self.past_hist.setPlaceholderText('Past History')
        self.past_hist.setTabChangesFocus(True)
        phvbox.addWidget(self.past_hist)
        # Add form to Group
        past_history_grp.setLayout(phvbox)
        # Add Group to Vbox
        self.vbox.addWidget(past_history_grp)

        # Female Specific
        # Menstrual History
        self.mens_hist = RTextEdit()
        self.mens_hist.setPlaceholderText('Menstrual History')
        self.mens_hist.setTabChangesFocus(True)
        # Leucorrhoea
        self.leucorrhoea = RTextEdit()
        self.leucorrhoea.setPlaceholderText('Leucorrhoea')
        self.leucorrhoea.setTabChangesFocus(True)
        # Gyenac History
        self.gynaec_hist = RTextEdit()
        self.gynaec_hist.setPlaceholderText('Gynaec History')
        self.gynaec_hist.setTabChangesFocus(True)
        if gender == 'F':

            female_history_grp = qt.QGroupBox('Female History')
            fhvform = qt.QFormLayout()
            fhvform.addRow(qt.QLabel('Menstrual History:  '), self.mens_hist)
            fhvform.addRow(qt.QLabel('Leucorrhoea:  '), self.leucorrhoea)
            fhvform.addRow(qt.QLabel('Gynaec History:  '), self.gynaec_hist)
            # Add Form to group
            female_history_grp.setLayout(fhvform)
            # Add group to Vbox
            self.vbox.addWidget(female_history_grp)

        # Children specific Queries
        # Teething
        self.ch_teething = RTextEdit()
        self.ch_teething.setPlaceholderText('Teething')
        self.ch_teething.setTabChangesFocus(True)
        # Crawling
        self.ch_crawling = RTextEdit()
        self.ch_crawling.setPlaceholderText('Crawling')
        self.ch_crawling.setTabChangesFocus(True)
        # Walking
        self.ch_walking = RTextEdit()
        self.ch_walking.setPlaceholderText('Walking')
        self.ch_walking.setTabChangesFocus(True)
        # Speaking
        self.ch_speaking = RTextEdit()
        self.ch_speaking.setPlaceholderText('Speaking')
        self.ch_speaking.setTabChangesFocus(True)
        # Vaccine
        self.ch_vaccine = RTextEdit()
        self.ch_vaccine.setPlaceholderText('Vaccine')
        self.ch_vaccine.setTabChangesFocus(True)
        # Head and Crown
        self.ch_headcrown = RTextEdit()
        self.ch_headcrown.setPlaceholderText('Head and Crown')
        self.ch_headcrown.setTabChangesFocus(True)
        if age < 15:
            # Child Milestone
            child_history_grp = qt.QGroupBox('Child History')
            chform = qt.QFormLayout()
            chform.addRow(qt.QLabel('Teething:  '), self.ch_teething)
            chform.addRow(qt.QLabel('Crawling:  '), self.ch_crawling)
            chform.addRow(qt.QLabel('Walking:  '), self.ch_walking)
            chform.addRow(qt.QLabel('Speaking:  '), self.ch_speaking)
            chform.addRow(qt.QLabel('Vaccine:  '), self.ch_vaccine)
            chform.addRow(qt.QLabel('Head and Crown:  '), self.ch_headcrown)
            # Add Form to Group
            child_history_grp.setLayout(chform)
            # Add group to vbox
            self.vbox.addWidget(child_history_grp)

        # Physical general
        physical_general_grp = qt.QGroupBox('Physical General')
        pgform = qt.QFormLayout()
        # Thermals
        self.pg_thermal = RTextEdit()
        self.pg_thermal.setPlaceholderText('Thermals')
        self.pg_thermal.setTabChangesFocus(True)
        pgform.addRow(qt.QLabel('Thermals:  '), self.pg_thermal)
        # Sun Sensitivity
        self.pg_sun = RTextEdit()
        self.pg_sun.setPlaceholderText('Sun Sensitivity')
        self.pg_sun.setTabChangesFocus(True)
        pgform.addRow(qt.QLabel('Sun Sensitivity:  '), self.pg_sun)
        # Thirst
        self.pg_thirst = RTextEdit()
        self.pg_thirst.setPlaceholderText('Thirst')
        self.pg_thirst.setTabChangesFocus(True)
        pgform.addRow(qt.QLabel('Thirst:  '), self.pg_thirst)
        # Tongue
        self.pg_tongue = RTextEdit()
        self.pg_tongue.setPlaceholderText('Tongue')
        self.pg_tongue.setTabChangesFocus(True)
        pgform.addRow(qt.QLabel('Tongue:  '), self.pg_tongue)
        # Appetite
        self.pg_appetite = RTextEdit()
        self.pg_appetite.setPlaceholderText('Appetite')
        self.pg_appetite.setTabChangesFocus(True)
        pgform.addRow(qt.QLabel('Appetite:  '), self.pg_appetite)
        # Hunger
        self.pg_hunger = RTextEdit()
        self.pg_hunger.setPlaceholderText('Hunger')
        self.pg_hunger.setTabChangesFocus(True)
        pgform.addRow(qt.QLabel('Hunger:  '), self.pg_hunger)
        # Desire
        self.pg_desire = RTextEdit()
        self.pg_desire.setPlaceholderText('Desire')
        self.pg_desire.setTabChangesFocus(True)
        pgform.addRow(qt.QLabel('Desire:  '), self.pg_desire)
        # Aversion
        self.pg_aversion = RTextEdit()
        self.pg_aversion.setPlaceholderText('Aversion')
        self.pg_aversion.setTabChangesFocus(True)
        pgform.addRow(qt.QLabel('Aversion:  '), self.pg_aversion)
        # Disagree
        self.pg_disagree = RTextEdit()
        self.pg_disagree.setPlaceholderText('Disagree')
        self.pg_disagree.setTabChangesFocus(True)
        pgform.addRow(qt.QLabel('Disagree:  '), self.pg_disagree)
        # Undigestable Things
        self.pg_undigestable = RTextEdit()
        self.pg_undigestable.setPlaceholderText('Undigestable Things')
        self.pg_undigestable.setTabChangesFocus(True)
        pgform.addRow(qt.QLabel('Undigestable Things:  '),
                      self.pg_undigestable)
        # Sleep
        self.pg_sleep = RTextEdit()
        self.pg_sleep.setPlaceholderText('Sleep')
        self.pg_sleep.setTabChangesFocus(True)
        pgform.addRow(qt.QLabel('Sleep:  '), self.pg_sleep)
        # Dreams
        self.pg_dreams = RTextEdit()
        self.pg_dreams.setPlaceholderText('Dreams')
        self.pg_dreams.setTabChangesFocus(True)
        pgform.addRow(qt.QLabel('Dreams:  '), self.pg_dreams)
        # Stool
        self.pg_stool = RTextEdit()
        self.pg_stool.setPlaceholderText('Stool')
        self.pg_stool.setTabChangesFocus(True)
        pgform.addRow(qt.QLabel('Stool:  '), self.pg_stool)
        # Urine
        self.pg_urine = RTextEdit()
        self.pg_urine.setPlaceholderText('Urine')
        self.pg_urine.setTabChangesFocus(True)
        pgform.addRow(qt.QLabel('Urine:  '), self.pg_urine)
        # Sweat
        self.pg_sweat = RTextEdit()
        self.pg_sweat.setPlaceholderText('Sweat')
        self.pg_sweat.setTabChangesFocus(True)
        pgform.addRow(qt.QLabel('Sweat:  '), self.pg_sweat)
        # Skin
        self.pg_skin = RTextEdit()
        self.pg_skin.setPlaceholderText('Skin')
        self.pg_skin.setTabChangesFocus(True)
        pgform.addRow(qt.QLabel('Skin:  '), self.pg_skin)
        # Nails
        self.pg_nails = RTextEdit()
        self.pg_nails.setPlaceholderText('Nails')
        self.pg_nails.setTabChangesFocus(True)
        pgform.addRow(qt.QLabel('Nails:  '), self.pg_nails)
        # Hobbies
        self.pg_hobbies = RTextEdit()
        self.pg_hobbies.setPlaceholderText('Hobbies')
        self.pg_hobbies.setTabChangesFocus(True)
        pgform.addRow(qt.QLabel('Hobbies:  '), self.pg_hobbies)
        # Addiction
        self.pg_addiction = RTextEdit()
        self.pg_addiction.setPlaceholderText('Addiction')
        self.pg_addiction.setTabChangesFocus(True)
        pgform.addRow(qt.QLabel('Addiction:  '), self.pg_addiction)
        # Speed
        self.pg_speed = RTextEdit()
        self.pg_speed.setPlaceholderText('Speed')
        self.pg_speed.setTabChangesFocus(True)
        pgform.addRow(qt.QLabel('Speed:  '), self.pg_speed)
        # Energy
        self.pg_energy = RTextEdit()
        self.pg_energy.setPlaceholderText('Energy')
        self.pg_energy.setTabChangesFocus(True)
        pgform.addRow(qt.QLabel('Energy:  '), self.pg_energy)
        # Sensitivity
        snsrow = qt.QHBoxLayout()
        # Smell
        self.pg_smell = RTextEdit()
        self.pg_smell.setPlaceholderText('Smell')
        self.pg_smell.setTabChangesFocus(True)
        snsrow.addWidget(self.pg_smell)
        # Taste
        self.pg_taste = RTextEdit()
        self.pg_taste.setPlaceholderText('Taste')
        self.pg_taste.setTabChangesFocus(True)
        snsrow.addWidget(self.pg_taste)
        # Touch
        self.pg_touch = RTextEdit()
        self.pg_touch.setPlaceholderText('Touch')
        self.pg_touch.setTabChangesFocus(True)
        snsrow.addWidget(self.pg_touch)
        # Vision
        self.pg_vision = RTextEdit()
        self.pg_vision.setPlaceholderText('Vision')
        self.pg_vision.setTabChangesFocus(True)
        snsrow.addWidget(self.pg_vision)
        # Hearning
        self.pg_hearing = RTextEdit()
        self.pg_hearing.setPlaceholderText('Hearning')
        self.pg_hearing.setTabChangesFocus(True)
        snsrow.addWidget(self.pg_hearing)
        pgform.addRow(qt.QLabel('Sensitivity:  '), snsrow)
        # Add from to group
        physical_general_grp.setLayout(pgform)
        # Add group to Vbox
        self.vbox.addWidget(physical_general_grp)

        # Family History
        family_history_grp = qt.QGroupBox('Family History')
        fhvbox = qt.QVBoxLayout()
        self.fam_hist = RTextEdit()
        self.fam_hist.setPlaceholderText('Family History')
        self.fam_hist.setTabChangesFocus(True)
        fhvbox.addWidget(self.fam_hist)
        # Add form to group
        family_history_grp.setLayout(fhvbox)
        # Add group to vbox
        self.vbox.addWidget(family_history_grp)

        # Mind and Disposition
        mind_disposition_grp = qt.QGroupBox('Mind and Disposition')
        mdform = qt.QFormLayout()
        # Childhood
        self.md_childhood = RTextEdit()
        self.md_childhood.setPlaceholderText('Childhood')
        self.md_childhood.setTabChangesFocus(True)
        mdform.addRow(qt.QLabel('Childhood:  '), self.md_childhood)
        # Education
        self.md_education = RTextEdit()
        self.md_education.setPlaceholderText('Education')
        self.md_education.setTabChangesFocus(True)
        mdform.addRow(qt.QLabel('Education:  '), self.md_education)
        # Marriage
        self.md_marriage = RTextEdit()
        self.md_marriage.setPlaceholderText('Marriage')
        self.md_marriage.setTabChangesFocus(True)
        mdform.addRow(qt.QLabel('Marriage:  '), self.md_marriage)
        # Children
        self.md_children = RTextEdit()
        self.md_children.setPlaceholderText('Children')
        self.md_children.setTabChangesFocus(True)
        mdform.addRow(qt.QLabel('Children:  '), self.md_children)
        # Expenses
        self.md_expenses = RTextEdit()
        self.md_expenses.setPlaceholderText('Expenses')
        self.md_expenses.setTabChangesFocus(True)
        mdform.addRow(qt.QLabel('Expenses:  '), self.md_expenses)
        # Religiousness
        self.md_religious = RTextEdit()
        self.md_religious.setPlaceholderText('Religiousness')
        self.md_religious.setTabChangesFocus(True)
        mdform.addRow(qt.QLabel('Religiousness:  '), self.md_religious)
        # Cleanliness
        self.md_cleanliness = RTextEdit()
        self.md_cleanliness.setPlaceholderText('Cleanliness')
        self.md_cleanliness.setTabChangesFocus(True)
        mdform.addRow(qt.QLabel('Cleanliness:  '), self.md_cleanliness)
        # Sympathy
        self.md_sympathy = RTextEdit()
        self.md_sympathy.setPlaceholderText('Sympathy')
        self.md_sympathy.setTabChangesFocus(True)
        mdform.addRow(qt.QLabel('Sympathy:  '), self.md_sympathy)
        # Anger
        self.md_anger = RTextEdit()
        self.md_anger.setPlaceholderText('Anger')
        self.md_anger.setTabChangesFocus(True)
        mdform.addRow(qt.QLabel('Anger:  '), self.md_anger)
        # Destruction
        self.md_destruction = RTextEdit()
        self.md_destruction.setPlaceholderText('Destruction')
        self.md_destruction.setTabChangesFocus(True)
        mdform.addRow(qt.QLabel('Destruction:  '), self.md_destruction)
        # Sexual History
        self.md_sexualhist = RTextEdit()
        self.md_sexualhist.setPlaceholderText('Sexual History')
        self.md_sexualhist.setTabChangesFocus(True)
        mdform.addRow(qt.QLabel('Sexual History:  '), self.md_sexualhist)
        # Future Plans
        self.md_futureplans = RTextEdit()
        self.md_futureplans.setPlaceholderText('Future Plans')
        self.md_futureplans.setTabChangesFocus(True)
        mdform.addRow(qt.QLabel('Future Plans:  '), self.md_futureplans)
        # Business
        self.md_business = RTextEdit()
        self.md_business.setPlaceholderText('Business')
        self.md_business.setTabChangesFocus(True)
        mdform.addRow(qt.QLabel('Business:  '), self.md_business)
        # Weeping
        self.md_weeping = RTextEdit()
        self.md_weeping.setPlaceholderText('Weeping')
        self.md_weeping.setTabChangesFocus(True)
        mdform.addRow(qt.QLabel('Weeping:  '), self.md_weeping)
        # During Illness
        self.md_illness = RTextEdit()
        self.md_illness.setPlaceholderText('During Illness')
        self.md_illness.setTabChangesFocus(True)
        mdform.addRow(qt.QLabel('During Illness:  '), self.md_illness)
        # Achievements
        self.md_achievements = RTextEdit()
        self.md_achievements.setPlaceholderText('Achievements')
        self.md_achievements.setTabChangesFocus(True)
        mdform.addRow(qt.QLabel('Achievements:  '), self.md_achievements)
        # During Holidays
        self.md_holidays = RTextEdit()
        self.md_holidays.setPlaceholderText('During Holidays')
        self.md_holidays.setTabChangesFocus(True)
        mdform.addRow(qt.QLabel('During Holidays:  '), self.md_holidays)
        # Add form to Group
        mind_disposition_grp.setLayout(mdform)
        # Add group to Vbox
        self.vbox.addWidget(mind_disposition_grp)

        # Current Medication
        current_medication_grp = qt.QGroupBox('Current Medication')
        cmvbox = qt.QVBoxLayout()
        self.cur_med = RTextEdit()
        self.cur_med.setPlaceholderText('Current Medication')
        self.cur_med.setTabChangesFocus(True)
        cmvbox.addWidget(self.cur_med)
        # Add form to group
        current_medication_grp.setLayout(cmvbox)
        # Add group to vbox
        self.vbox.addWidget(current_medication_grp)

        # Accutes
        accutes_grp = qt.QGroupBox('Accutes')
        acvbox = qt.QVBoxLayout()
        self.accute = RTextEdit()
        self.accute.setPlaceholderText('Accutes')
        self.accute.setTabChangesFocus(True)
        acvbox.addWidget(self.accute)
        # Add form to group
        accutes_grp.setLayout(acvbox)
        # Add group to vbox
        self.vbox.addWidget(accutes_grp)

        # Final Prescription
        final_prescription_grp = qt.QGroupBox('Prescription')
        fpform = qt.QFormLayout()
        # Totality
        self.fp_totality = RTextEdit()
        self.fp_totality.setPlaceholderText('Totality')
        self.fp_totality.setTabChangesFocus(True)
        fpform.addRow(qt.QLabel('Totality:  '), self.fp_totality)
        # Rubrics
        self.fp_rubrics = RTextEdit()
        self.fp_rubrics.setPlaceholderText('Rubrics')
        self.fp_rubrics.setTabChangesFocus(True)
        fpform.addRow(qt.QLabel('Rubrics:  '), self.fp_rubrics)
        # Prescription + Potency
        self.fp_prescription = RTextEdit()
        self.fp_prescription.setPlaceholderText('Prescription + Potency')
        self.fp_prescription.setTabChangesFocus(True)
        fpform.addRow(qt.QLabel('Prescription + Potency:  '),
                      self.fp_prescription)
        # D/D
        self.fp_dd = RTextEdit()
        self.fp_dd.setPlaceholderText('D/D')
        self.fp_dd.setTabChangesFocus(True)
        fpform.addRow(qt.QLabel('D/D:  '), self.fp_dd)
        # Add form to Group
        final_prescription_grp.setLayout(fpform)
        # Add Group to Vbox
        self.vbox.addWidget(final_prescription_grp)

        # Button to save Case
        submit_row = qt.QHBoxLayout()
        save = qt.QPushButton('Save')
        save.setIcon(gui.QIcon(settings['save']))
        save.setIconSize(core.QSize(24, 24))
        save.setFlat(True)
        save.setToolTip('Save Case')
        save.clicked.connect(self.save_case)
        submit_row.addStretch()
        submit_row.addWidget(save)
        self.vbox.addLayout(submit_row)

        # Get latest case and populate
        self.populate_case()

        # Set Scroll Area
        scroll_widget.setLayout(self.vbox)
        scroll_win.setWidget(scroll_widget)

        outer_box.addWidget(scroll_win)
        # Set Layout
        self.setLayout(outer_box)

        # Display Window
        self.setWindowTitle('Case - {} {}'.format(fname, lname))
        self.setModal(True)
        self.showMaximized()
        self.setWindowIcon(settings["icon"])
        self.exec()

    def populate_case(self):
        patient_case = self.casedb.get_case_by_patient(self.pid)

        if patient_case:
            self.cc_location.setText(patient_case[0])
            self.cc_sensation.setText(patient_case[1])
            self.cc_aggravation.setText(patient_case[2])
            self.cc_amelioration.setText(patient_case[3])
            self.cc_concometent.setText(patient_case[4])
            self.cc_allopathymed.setText(patient_case[5])
            self.past_hist.setText(patient_case[12])
            self.mens_hist.setText(patient_case[13])
            self.leucorrhoea.setText(patient_case[14])
            self.gynaec_hist.setText(patient_case[15])
            self.pg_appetite.setText(patient_case[16])
            self.pg_thermal.setText(patient_case[17])
            self.pg_thirst.setText(patient_case[18])
            self.pg_aversion.setText(patient_case[19])
            self.pg_disagree.setText(patient_case[20])
            self.pg_undigestable.setText(patient_case[21])
            self.pg_hunger.setText(patient_case[22])
            self.pg_stool.setText(patient_case[23])
            self.pg_urine.setText(patient_case[24])
            self.pg_sweat.setText(patient_case[25])
            self.pg_sleep.setText(patient_case[26])
            self.pg_dreams.setText(patient_case[27])
            self.pg_skin.setText(patient_case[28])
            self.pg_nails.setText(patient_case[29])
            self.pg_hobbies.setText(patient_case[30])
            self.pg_addiction.setText(patient_case[31])
            self.pg_smell.setText(patient_case[32])
            self.pg_taste.setText(patient_case[33])
            self.pg_touch.setText(patient_case[34])
            self.pg_vision.setText(patient_case[35])
            self.pg_hearing.setText(patient_case[36])
            self.fam_hist.setText(patient_case[37])
            self.md_childhood.setText(patient_case[38])
            self.md_education.setText(patient_case[39])
            self.md_marriage.setText(patient_case[40])
            self.md_children.setText(patient_case[41])
            self.md_expenses.setText(patient_case[42])
            self.md_religious.setText(patient_case[43])
            self.md_cleanliness.setText(patient_case[44])
            self.md_sympathy.setText(patient_case[45])
            self.md_anger.setText(patient_case[46])
            self.md_destruction.setText(patient_case[47])
            self.md_sexualhist.setText(patient_case[48])
            self.md_futureplans.setText(patient_case[49])
            self.md_business.setText(patient_case[50])
            self.md_weeping.setText(patient_case[51])
            self.md_illness.setText(patient_case[52])
            self.md_achievements.setText(patient_case[53])
            self.md_holidays.setText(patient_case[54])
            self.ch_teething.setText(patient_case[55])
            self.ch_crawling.setText(patient_case[56])
            self.ch_walking.setText(patient_case[57])
            self.ch_speaking.setText(patient_case[58])
            self.ch_vaccine.setText(patient_case[59])
            self.ch_headcrown.setText(patient_case[60])
            self.cur_med.setText(patient_case[61])
            self.accute.setText(patient_case[62])
            self.fp_totality.setText(patient_case[63])
            self.fp_rubrics.setText(patient_case[64])
            self.fp_prescription.setText(patient_case[65])
            self.pg_desire.setText(patient_case[66])
            self.pg_tongue.setText(patient_case[67])
            self.pg_speed.setText(patient_case[68])
            self.pg_energy.setText(patient_case[69])
            self.fp_dd.setText(patient_case[70])
            self.pg_sun.setText(patient_case[71])

            # Create associated complaints
            if patient_case[6] != '' or patient_case[7] != '' or patient_case[8] != '' \
                    or patient_case[9] != '' or patient_case[10] != '' or patient_case[11] != '':
                ac_loc = patient_case[6].split('|')
                ac_sen = patient_case[7].split('|')
                ac_agg = patient_case[8].split('|')
                ac_ame = patient_case[9].split('|')
                ac_con = patient_case[10].split('|')
                ac_alp = patient_case[11].split('|')
                for asso_compl in zip(ac_loc, ac_sen, ac_ame, ac_agg, ac_con, ac_alp):
                    self.add_associated_complaint(*asso_compl)

    def add_associated_complaint(self, ac_loc=None, ac_sen=None, ac_ame=None, ac_agg=None, ac_con=None, ac_alp=None):
        ac_id = len(self.associated_complaint_list.keys())

        asso_complaint_grp = qt.QGroupBox()
        assoc_vbox = qt.QVBoxLayout()
        acform = qt.QHBoxLayout()
        # Delete Button
        del_btn = qt.QPushButton('')
        del_btn.setIcon(gui.QIcon(settings['delete_icon']))
        del_btn.setFlat(True)
        del_btn.clicked.connect(
            partial(self.remove_associated_complaint, ac_id)
        )
        btn_row = qt.QHBoxLayout()
        btn_row.addWidget(del_btn)
        btn_row.addStretch()
        # Add Delete button row to next row
        assoc_vbox.addLayout(btn_row)
        # Complaint Location
        ac_location = RTextEdit()
        ac_location.setPlaceholderText('Location')
        ac_location.setTabChangesFocus(True)
        if ac_loc:
            ac_location.setText(ac_loc)
        ac_loc_col = qt.QVBoxLayout()
        ac_loc_col.addWidget(qt.QLabel('Location'))
        ac_loc_col.addWidget(ac_location)
        ac_loc_col.setAlignment(core.Qt.AlignTop)
        acform.addLayout(ac_loc_col)
        # Complaint Sensation
        ac_sensation = RTextEdit()
        ac_sensation.setPlaceholderText('Sensation')
        ac_sensation.setTabChangesFocus(True)
        if ac_sen:
            ac_sensation.setText(ac_sen)
        ac_sen_col = qt.QVBoxLayout()
        ac_sen_col.addWidget(qt.QLabel('Sensation'))
        ac_sen_col.addWidget(ac_sensation)
        ac_sen_col.setAlignment(core.Qt.AlignTop)
        acform.addLayout(ac_sen_col)
        # Modality
        ac_amelioration = RTextEdit()
        ac_amelioration.setPlaceholderText('Amelioration')
        ac_amelioration.setTabChangesFocus(True)
        if ac_ame:
            ac_amelioration.setText(ac_ame)
        ac_aggravation = RTextEdit()
        ac_aggravation.setPlaceholderText('Aggravation')
        ac_aggravation.setTabChangesFocus(True)
        if ac_agg:
            ac_aggravation.setText(ac_agg)
        ac_mod_col = qt.QVBoxLayout()
        ac_mod_col.addWidget(qt.QLabel('Modality'))
        ac_mod_col.addWidget(ac_aggravation)
        ac_mod_col.addWidget(ac_amelioration)
        ac_mod_col.setAlignment(core.Qt.AlignTop)
        acform.addLayout(ac_mod_col)
        # Concometent
        ac_concometent = RTextEdit()
        ac_concometent.setPlaceholderText('Concomitant')
        ac_concometent.setTabChangesFocus(True)
        if ac_con:
            ac_concometent.setText(ac_con)
        ac_conc_col = qt.QVBoxLayout()
        ac_conc_col.addWidget(qt.QLabel('Concomitant'))
        ac_conc_col.addWidget(ac_concometent)
        ac_conc_col.setAlignment(core.Qt.AlignTop)
        acform.addLayout(ac_conc_col)
        # Add Horizontal form to vertical 1st row
        assoc_vbox.addLayout(acform)
        # Allopathy Medicine
        ac_allop_form = qt.QFormLayout()
        ac_allopathymed = RTextEdit()
        ac_allopathymed.setPlaceholderText('Allopathy Medicine')
        ac_allopathymed.setTabChangesFocus(True)
        if ac_alp:
            ac_allopathymed.setText(ac_alp)
        ac_allop_form.addRow(
            qt.QLabel('Allopathy Medicine:  '),
            ac_allopathymed
        )
        assoc_vbox.addLayout(ac_allop_form)
        # Add form to Group
        asso_complaint_grp.setLayout(assoc_vbox)
        # Add Buttons to List
        self.associated_complaint_list[ac_id] = (
            ac_location, ac_sensation, ac_amelioration, ac_aggravation, ac_concometent, ac_allopathymed)
        self.associated_complaint_widgets[ac_id] = asso_complaint_grp

        # Add to Vox
        self.assocVbox.addWidget(asso_complaint_grp)

        # Update VBox
        self.assocVbox.update()

    def remove_associated_complaint(self, id):
        self.associated_complaint_widgets[id].setParent(None)
        del(self.associated_complaint_widgets[id])
        del(self.associated_complaint_list[id])
        self.assocVbox.update()

    def set_validators(self):
        string_validator_re = core.QRegExp(
            r'[A-Za-z0-9\s\(\)\[\]\?\,\.\<\>\%]+')
        self.string_validator = gui.QRegExpValidator(string_validator_re)

    def save_case(self):
        if self.pid is None or self.pid == '':
            MsgErrBox('Patient not found')
        else:
            cc_loc = self.cc_location.getText().replace("'", "''")
            cc_sen = self.cc_sensation.getText().replace("'", "''")
            cc_ame = self.cc_amelioration.getText().replace("'", "''")
            cc_agg = self.cc_aggravation.getText().replace("'", "''")
            cc_con = self.cc_concometent.getText().replace("'", "''")
            cc_alp = self.cc_allopathymed.getText().replace("'", "''")
            aclitm = self.associated_complaint_list.items()
            # Location in 0th position of value
            ac_loc = "|".join([acl[1][0].getText()
                               for acl in aclitm]).replace("'", "''")
            # Sensation in 1st position of value
            ac_sen = "|".join([acl[1][1].getText()
                               for acl in aclitm]).replace("'", "''")
            # Amelioration in 2nd position of value
            ac_ame = "|".join([acl[1][2].getText()
                               for acl in aclitm]).replace("'", "''")
            # Aggravation in 3rd position of value
            ac_agg = "|".join([acl[1][3].getText()
                               for acl in aclitm]).replace("'", "''")
            # Concometent in 4th position of value
            ac_con = "|".join([acl[1][4].getText()
                               for acl in aclitm]).replace("'", "''")
            # Allopathy Medicine in 5th position of value
            ac_alp = "|".join([acl[1][5].getText()
                               for acl in aclitm]).replace("'", "''")
            pahist = self.past_hist.getText().replace("'", "''")
            mehist = self.mens_hist.getText().replace("'", "''")
            leucor = self.leucorrhoea.getText().replace("'", "''")
            gynaec = self.gynaec_hist.getText().replace("'", "''")
            pg_app = self.pg_appetite.getText().replace("'", "''")
            pg_the = self.pg_thermal.getText().replace("'", "''")
            pg_thi = self.pg_thirst.getText().replace("'", "''")
            pg_ave = self.pg_aversion.getText().replace("'", "''")
            pg_dis = self.pg_disagree.getText().replace("'", "''")
            pg_und = self.pg_undigestable.getText().replace("'", "''")
            pg_hng = self.pg_hunger.getText().replace("'", "''")
            pg_stl = self.pg_stool.getText().replace("'", "''")
            pg_urn = self.pg_urine.getText().replace("'", "''")
            pg_swt = self.pg_sweat.getText().replace("'", "''")
            pg_slp = self.pg_sleep.getText().replace("'", "''")
            pg_drm = self.pg_dreams.getText().replace("'", "''")
            pg_skn = self.pg_skin.getText().replace("'", "''")
            pg_nls = self.pg_nails.getText().replace("'", "''")
            pg_hbs = self.pg_hobbies.getText().replace("'", "''")
            pg_adc = self.pg_addiction.getText().replace("'", "''")
            pg_sml = self.pg_smell.getText().replace("'", "''")
            pg_tst = self.pg_taste.getText().replace("'", "''")
            pg_tou = self.pg_touch.getText().replace("'", "''")
            pg_vis = self.pg_vision.getText().replace("'", "''")
            pg_hrn = self.pg_hearing.getText().replace("'", "''")
            famhst = self.fam_hist.getText().replace("'", "''")
            md_chd = self.md_childhood.getText().replace("'", "''")
            md_edu = self.md_education.getText().replace("'", "''")
            md_mar = self.md_marriage.getText().replace("'", "''")
            md_crn = self.md_children.getText().replace("'", "''")
            md_exp = self.md_expenses.getText().replace("'", "''")
            md_rlg = self.md_religious.getText().replace("'", "''")
            md_cln = self.md_cleanliness.getText().replace("'", "''")
            md_sym = self.md_sympathy.getText().replace("'", "''")
            md_agr = self.md_anger.getText().replace("'", "''")
            md_dst = self.md_destruction.getText().replace("'", "''")
            md_sxh = self.md_sexualhist.getText().replace("'", "''")
            md_fpl = self.md_futureplans.getText().replace("'", "''")
            md_bsn = self.md_business.getText().replace("'", "''")
            md_wpn = self.md_weeping.getText().replace("'", "''")
            md_ill = self.md_illness.getText().replace("'", "''")
            md_ach = self.md_achievements.getText().replace("'", "''")
            md_hld = self.md_holidays.getText().replace("'", "''")
            ch_tth = self.ch_teething.getText().replace("'", "''")
            ch_crl = self.ch_crawling.getText().replace("'", "''")
            ch_wlk = self.ch_walking.getText().replace("'", "''")
            ch_spk = self.ch_speaking.getText().replace("'", "''")
            ch_vcn = self.ch_vaccine.getText().replace("'", "''")
            ch_hcr = self.ch_headcrown.getText().replace("'", "''")
            curmed = self.cur_med.getText().replace("'", "''")
            accute = self.accute.getText().replace("'", "''")
            fp_ttl = self.fp_totality.getText().replace("'", "''")
            fp_rbr = self.fp_rubrics.getText().replace("'", "''")
            fp_prs = self.fp_prescription.getText().replace("'", "''")
            pg_des = self.pg_desire.getText().replace("'", "''")
            pg_ton = self.pg_tongue.getText().replace("'", "''")
            pg_spd = self.pg_speed.getText().replace("'", "''")
            pg_eng = self.pg_energy.getText().replace("'", "''")
            fp_dds = self.fp_dd.getText().replace("'", "''")
            pg_sun = self.pg_sun.getText().replace("'", "''")

            # Save Case
            case_id = self.casedb.save_case(self.pid,
                                            cc_loc,
                                            cc_sen,
                                            cc_ame,
                                            cc_agg,
                                            cc_con,
                                            cc_alp,
                                            ac_loc,
                                            ac_sen,
                                            ac_ame,
                                            ac_agg,
                                            ac_con,
                                            ac_alp,
                                            pahist,
                                            mehist,
                                            leucor,
                                            gynaec,
                                            pg_app,
                                            pg_the,
                                            pg_thi,
                                            pg_ave,
                                            pg_dis,
                                            pg_und,
                                            pg_hng,
                                            pg_stl,
                                            pg_urn,
                                            pg_swt,
                                            pg_slp,
                                            pg_drm,
                                            pg_skn,
                                            pg_nls,
                                            pg_hbs,
                                            pg_adc,
                                            pg_sml,
                                            pg_tst,
                                            pg_tou,
                                            pg_vis,
                                            pg_hrn,
                                            famhst,
                                            md_chd,
                                            md_edu,
                                            md_mar,
                                            md_crn,
                                            md_exp,
                                            md_rlg,
                                            md_cln,
                                            md_sym,
                                            md_agr,
                                            md_dst,
                                            md_sxh,
                                            md_fpl,
                                            md_bsn,
                                            md_wpn,
                                            md_ill,
                                            md_ach,
                                            md_hld,
                                            ch_tth,
                                            ch_crl,
                                            ch_wlk,
                                            ch_spk,
                                            ch_vcn,
                                            ch_hcr,
                                            curmed,
                                            accute,
                                            fp_ttl,
                                            fp_rbr,
                                            fp_prs,
                                            pg_des,
                                            pg_ton,
                                            pg_spd,
                                            pg_eng,
                                            fp_dds,
                                            pg_sun)

            case = self.casedb.get_case_by_id(case_id)

            # print(case_id)
            # print(case)

            if case:
                self.case_saved = True
                self.close()
                MsgSucBox('Case Saved Successfully')
            else:
                MsgErrBox('Unable to Save Case')

    def closeEvent(self, event):
        if self.case_saved:
            event.accept()
        else:
            MsgCloseConfirm(self.save_case, self.close, event.ignore).confirm()


class ViewCase(qt.QDialog):
    def __init__(self):
        super().__init__()

        # Db Connection
        self.patndb = PatientDB()
        self.casedb = CaseDB()

        # Set Stylesheet
        self.setStyleSheet(settings["theme"])

    def view_case(self, patient_id, case_id=None):
        patient = self.patndb.get_patient_by_id(patient_id)
        if case_id:
            case = self.casedb.get_case_by_id(case_id)
        else:
            case = self.casedb.get_case_by_patient(patient_id)

        # print(case)

        # Scroll Widget
        scroll_layout = qt.QVBoxLayout()
        scroll_widget = qt.QWidget()
        scroll_win = qt.QScrollArea()
        scroll_win.setVerticalScrollBarPolicy(core.Qt.ScrollBarAlwaysOn)
        scroll_win.setHorizontalScrollBarPolicy(core.Qt.ScrollBarAlwaysOff)
        scroll_win.setWidgetResizable(True)

        vbox = qt.QVBoxLayout()

        # Patient Group Box
        patn_grp = qt.QGroupBox('Patient')

        # Create Form Layout
        patnform = qt.QFormLayout()

        # Generate form
        # Patient Name
        patnform.addRow(
            qt.QLabel('Patient Name:  '),
            qt.QLabel(patient[1] + ' ' + patient[2])
        )

        # Age
        cur_yr = date.today().year
        age = cur_yr - patient[3]
        patnform.addRow(
            qt.QLabel('Age:  '),
            qt.QLabel(str(age))
        )

        # Gender
        if patient[4] == 'M':
            gender = 'Male'
        elif patient[4] == 'F':
            gender = 'Female'
        else:
            gender = 'Other'
        patnform.addRow(
            qt.QLabel('Gender:  '),
            qt.QLabel(gender)
        )

        # Phone
        patnform.addRow(
            qt.QLabel('Phone:  '),
            qt.QLabel(patient[5])
        )

        # Address
        patnform.addRow(
            qt.QLabel('Address:  '),
            qt.QLabel(patient[6])
        )

        # Occupation
        patnform.addRow(
            qt.QLabel('Occupation:  '),
            qt.QLabel(patient[7])
        )

        # Marital Status
        if patient[8] == 'S':
            marstat = 'Single'
        elif patient[8] == 'M':
            marstat = 'Married'
        else:
            marstat = 'Undisclosed'
        patnform.addRow(
            qt.QLabel('Marital Status:  '),
            qt.QLabel(marstat)
        )

        # Reference
        patnform.addRow(
            qt.QLabel('Referred By:  '),
            qt.QLabel(patient[9])
        )

        patn_grp.setLayout(patnform)

        vbox.addWidget(patn_grp)

        # Check if patient has any case
        if case is not None:
            # Case Information
            # Chief Complaint
            cc_group = qt.QGroupBox('Chief Complaint')
            cc_col = qt.QVBoxLayout()
            cc_row = qt.QHBoxLayout()
            cc_loc_group = qt.QGroupBox('Location')
            cc_loc_vbox = qt.QVBoxLayout()
            cc_loc_vbox.addWidget(qt.QLabel(case[0]))
            cc_loc_vbox.setAlignment(core.Qt.AlignTop)
            cc_loc_group.setLayout(cc_loc_vbox)
            cc_loc_group.setMinimumWidth(200)

            cc_sen_group = qt.QGroupBox('Sensation')
            cc_sen_vbox = qt.QVBoxLayout()
            cc_sen_vbox.addWidget(qt.QLabel(case[1]))
            cc_sen_vbox.setAlignment(core.Qt.AlignTop)
            cc_sen_group.setLayout(cc_sen_vbox)

            cc_mod_group = qt.QGroupBox('Modality')
            cc_mod_vbox = qt.QVBoxLayout()
            cc_agg_row = qt.QHBoxLayout()
            cc_agg_row.addWidget(qt.QLabel('Aggravation:  '))
            cc_agg_row.addWidget(qt.QLabel(case[2]))
            cc_agg_row.addStretch()
            cc_mod_vbox.addLayout(cc_agg_row)
            cc_mod_vbox.addWidget(QHSeperationLine())
            cc_ame_row = qt.QHBoxLayout()
            cc_ame_row.addWidget(qt.QLabel('Amelioration:  '))
            cc_ame_row.addWidget(qt.QLabel(case[3]))
            cc_ame_row.addStretch()
            cc_mod_vbox.addLayout(cc_ame_row)
            cc_mod_vbox.setAlignment(core.Qt.AlignTop)
            cc_mod_group.setLayout(cc_mod_vbox)

            cc_con_group = qt.QGroupBox('Concomitant')
            cc_con_vbox = qt.QVBoxLayout()
            cc_con_vbox.addWidget(qt.QLabel(case[4]))
            cc_con_vbox.setAlignment(core.Qt.AlignTop)
            cc_con_group.setLayout(cc_con_vbox)

            cc_row.addWidget(cc_loc_group)
            # cc_row.addStretch()
            cc_row.addWidget(cc_sen_group)
            # cc_row.addStretch()
            cc_row.addWidget(cc_mod_group)
            # cc_row.addStretch()
            cc_row.addWidget(cc_con_group)
            cc_col.addLayout(cc_row)

            # Show Allopathy Medicine
            cc_alm = qt.QHBoxLayout()
            cc_alm.addWidget(qt.QLabel('Allopathy Medicine:  '))
            cc_alm.addWidget(qt.QLabel(case[5]))
            cc_alm.addStretch()
            cc_col.addLayout(cc_alm)
            cc_group.setLayout(cc_col)

            vbox.addWidget(cc_group)

            # Associated Complaint
            if case[6] != '' or case[7] != '' or case[8] != '' or case[9] != '' or case[10] != '' or case[11] != '':
                ac_group = qt.QGroupBox('Associated Complaints')
                ac_vbox = qt.QVBoxLayout()
                ac_loc = case[6].split('|')
                ac_sen = case[7].split('|')
                ac_agg = case[8].split('|')
                ac_ame = case[9].split('|')
                ac_con = case[10].split('|')
                ac_alp = case[11].split('|')

                ac_row = []
                ac_loc_group = []
                ac_sen_group = []
                ac_mod_group = []
                ac_con_group = []
                ac_loc_vbox = []
                ac_sen_vbox = []
                ac_mod_vbox = []
                ac_con_vbox = []

                for ac_num, (ac_loc_data, ac_sen_data, ac_ame_data, ac_agg_data, ac_con_data, ac_alp_data) \
                        in enumerate(zip(ac_loc, ac_sen, ac_ame, ac_agg, ac_con, ac_alp)):
                    ac_row.append(qt.QHBoxLayout())
                    ac_loc_group.append(qt.QGroupBox('Location'))
                    ac_loc_vbox.append(qt.QVBoxLayout())
                    ac_loc_vbox[ac_num].addWidget(qt.QLabel(ac_loc_data))
                    ac_loc_vbox[ac_num].setAlignment(core.Qt.AlignTop)
                    ac_loc_group[ac_num].setLayout(ac_loc_vbox[ac_num])
                    # ac_loc_group.setMinimumHeight(200)

                    ac_sen_group.append(qt.QGroupBox('Sensation'))
                    ac_sen_vbox.append(qt.QVBoxLayout())
                    ac_sen_vbox[ac_num].addWidget(qt.QLabel(ac_sen_data))
                    ac_sen_vbox[ac_num].setAlignment(core.Qt.AlignTop)
                    ac_sen_group[ac_num].setLayout(ac_sen_vbox[ac_num])
                    # ac_sen_group.setMinimumHeight(200)

                    ac_mod_group.append(qt.QGroupBox('Modality'))
                    ac_mod_vbox.append(qt.QVBoxLayout())
                    ac_agg_row = qt.QHBoxLayout()
                    ac_agg_row.addWidget(qt.QLabel('Aggravation:  '))
                    ac_agg_row.addWidget(qt.QLabel(ac_agg_data))
                    ac_agg_row.addStretch()
                    ac_mod_vbox[ac_num].addLayout(ac_agg_row)
                    ac_mod_vbox[ac_num].addWidget(QHSeperationLine())
                    ac_ame_row = qt.QHBoxLayout()
                    ac_ame_row.addWidget(qt.QLabel('Amelioration:  '))
                    ac_ame_row.addWidget(qt.QLabel(ac_ame_data))
                    ac_ame_row.addStretch()
                    ac_mod_vbox[ac_num].addLayout(ac_ame_row)
                    ac_mod_vbox[ac_num].setAlignment(core.Qt.AlignTop)
                    ac_mod_group[ac_num].setLayout(ac_mod_vbox[ac_num])
                    # ac_mod_group.setMinimumHeight(200)

                    ac_con_group.append(qt.QGroupBox('Concomitant'))
                    ac_con_vbox.append(qt.QVBoxLayout())
                    ac_con_vbox[ac_num].addWidget(qt.QLabel(ac_con_data))
                    ac_con_vbox[ac_num].setAlignment(core.Qt.AlignTop)
                    ac_con_group[ac_num].setLayout(ac_con_vbox[ac_num])
                    # ac_con_group.setMinimumHeight(200)

                    ac_row[ac_num].addWidget(ac_loc_group[ac_num])
                    # ac_row.addStretch()
                    ac_row[ac_num].addWidget(ac_sen_group[ac_num])
                    # ac_row.addStretch()
                    ac_row[ac_num].addWidget(ac_mod_group[ac_num])
                    # ac_row.addStretch()
                    ac_row[ac_num].addWidget(ac_con_group[ac_num])

                    ac_vbox.addLayout(ac_row[ac_num])
                    ac_alm = qt.QHBoxLayout()
                    ac_alm.addWidget(qt.QLabel('Allopathy Medicine:  '))
                    ac_alm.addWidget(qt.QLabel(ac_alp_data))
                    ac_alm.addStretch()
                    ac_vbox.addLayout(ac_alm)
                    if ac_num < len(ac_loc) - 1:
                        ac_vbox.addWidget(QHSeperationLine())

                ac_group.setLayout(ac_vbox)
                vbox.addWidget(ac_group)

            # Past History
            ph_grp = qt.QGroupBox('Past History')
            ph_row = qt.QVBoxLayout()
            ph_data = case[12]
            ph_row.addWidget(qt.QLabel(ph_data))
            ph_grp.setLayout(ph_row)
            vbox.addWidget(ph_grp)

            # Female History
            if patient[4] == 'F':
                mh_grp = qt.QGroupBox('Female History')
                mh_form = qt.QFormLayout()

                mh_form.addRow(
                    qt.QLabel('Menstrual History:  '),
                    qt.QLabel(case[13])
                )

                mh_form.addRow(
                    qt.QLabel('Leucorrhoea:  '),
                    qt.QLabel(case[14])
                )

                mh_form.addRow(
                    qt.QLabel('Gyaneac History:  '),
                    qt.QLabel(case[15])
                )

                mh_grp.setLayout(mh_form)
                vbox.addWidget(mh_grp)

            # Childhood history for children
            if age < 15:
                ch_grp = qt.QGroupBox('Childhood Milestones')
                ch_form = qt.QFormLayout()

                ch_form.addRow(
                    qt.QLabel('Teething:  '),
                    qt.QLabel(case[55])
                )
                ch_form.addRow(
                    qt.QLabel('Crawling:  '),
                    qt.QLabel(case[56])
                )
                ch_form.addRow(
                    qt.QLabel('Walking:  '),
                    qt.QLabel(case[57])
                )
                ch_form.addRow(
                    qt.QLabel('Speaking:  '),
                    qt.QLabel(case[58])
                )
                ch_form.addRow(
                    qt.QLabel('Vaccine:  '),
                    qt.QLabel(case[59])
                )
                ch_form.addRow(
                    qt.QLabel('Head and Crown:  '),
                    qt.QLabel(case[60])
                )

                ch_grp.setLayout(ch_form)
                vbox.addWidget(ch_grp)

            # Physical General
            pg_grp = qt.QGroupBox('Physical General')
            pg_form = qt.QFormLayout()

            pg_form.addRow(
                qt.QLabel('Thermals:  '),
                qt.QLabel(case[17])
            )
            pg_form.addRow(
                qt.QLabel('Sun Sensitivity:  '),
                qt.QLabel(case[71])
            )
            pg_form.addRow(
                qt.QLabel('Thirst:  '),
                qt.QLabel(case[18])
            )
            pg_form.addRow(
                qt.QLabel('Tongue:  '),
                qt.QLabel(case[67])
            )
            pg_form.addRow(
                qt.QLabel('Appetite:  '),
                qt.QLabel(case[16])
            )
            pg_form.addRow(
                qt.QLabel('Hunger:  '),
                qt.QLabel(case[22])
            )
            pg_form.addRow(
                qt.QLabel('Desire:  '),
                qt.QLabel(case[66])
            )
            pg_form.addRow(
                qt.QLabel('Aversion:  '),
                qt.QLabel(case[19])
            )
            pg_form.addRow(
                qt.QLabel('Disagree:  '),
                qt.QLabel(case[20])
            )
            pg_form.addRow(
                qt.QLabel('Undigestable Things:  '),
                qt.QLabel(case[21])
            )
            pg_form.addRow(
                qt.QLabel('Sleep:  '),
                qt.QLabel(case[26])
            )
            pg_form.addRow(
                qt.QLabel('Dreams:  '),
                qt.QLabel(case[27])
            )
            pg_form.addRow(
                qt.QLabel('Stool:  '),
                qt.QLabel(case[23])
            )
            pg_form.addRow(
                qt.QLabel('Urine:  '),
                qt.QLabel(case[24])
            )
            pg_form.addRow(
                qt.QLabel('Sweat:  '),
                qt.QLabel(case[25])
            )
            pg_form.addRow(
                qt.QLabel('Skin:  '),
                qt.QLabel(case[28])
            )
            pg_form.addRow(
                qt.QLabel('Nails:  '),
                qt.QLabel(case[29])
            )
            pg_form.addRow(
                qt.QLabel('Hobbies:  '),
                qt.QLabel(case[30])
            )
            pg_form.addRow(
                qt.QLabel('Addiction:  '),
                qt.QLabel(case[31])
            )
            pg_form.addRow(
                qt.QLabel('Speed:  '),
                qt.QLabel(case[68])
            )
            pg_form.addRow(
                qt.QLabel('Energy:  '),
                qt.QLabel(case[69])
            )
            pg_form.addRow(
                qt.QLabel('Smell:  '),
                qt.QLabel(case[32])
            )
            pg_form.addRow(
                qt.QLabel('Taste:  '),
                qt.QLabel(case[33])
            )
            pg_form.addRow(
                qt.QLabel('Touch:  '),
                qt.QLabel(case[34])
            )
            pg_form.addRow(
                qt.QLabel('Vision:  '),
                qt.QLabel(case[35])
            )
            pg_form.addRow(
                qt.QLabel('Hearing:  '),
                qt.QLabel(case[36])
            )

            pg_grp.setLayout(pg_form)
            vbox.addWidget(pg_grp)

            # Family History
            fh_grp = qt.QGroupBox('Family History')
            fh_form = qt.QFormLayout()

            fh_form.addRow(
                qt.QLabel('Family History:  '),
                qt.QLabel(case[37])
            )

            fh_grp.setLayout(fh_form)
            vbox.addWidget(fh_grp)

            # Mind and Disposition
            md_grp = qt.QGroupBox('Mind and Disposition')
            md_form = qt.QFormLayout()

            md_form.addRow(
                qt.QLabel('Childhood:  '),
                qt.QLabel(case[38])
            )
            md_form.addRow(
                qt.QLabel('Education:  '),
                qt.QLabel(case[39])
            )
            md_form.addRow(
                qt.QLabel('Marriage:  '),
                qt.QLabel(case[40])
            )
            md_form.addRow(
                qt.QLabel('Children:  '),
                qt.QLabel(case[41])
            )
            md_form.addRow(
                qt.QLabel('Expenses:  '),
                qt.QLabel(case[42])
            )
            md_form.addRow(
                qt.QLabel('Religious:  '),
                qt.QLabel(case[43])
            )
            md_form.addRow(
                qt.QLabel('Cleanliness:  '),
                qt.QLabel(case[44])
            )
            md_form.addRow(
                qt.QLabel('Sympathy:  '),
                qt.QLabel(case[45])
            )
            md_form.addRow(
                qt.QLabel('Anger:  '),
                qt.QLabel(case[46])
            )
            md_form.addRow(
                qt.QLabel('Destruction:  '),
                qt.QLabel(case[47])
            )
            md_form.addRow(
                qt.QLabel('Sexual History:  '),
                qt.QLabel(case[48])
            )
            md_form.addRow(
                qt.QLabel('Future Plans:  '),
                qt.QLabel(case[49])
            )
            md_form.addRow(
                qt.QLabel('Business:  '),
                qt.QLabel(case[50])
            )
            md_form.addRow(
                qt.QLabel('Weeping:  '),
                qt.QLabel(case[51])
            )
            md_form.addRow(
                qt.QLabel('During Illness:  '),
                qt.QLabel(case[52])
            )
            md_form.addRow(
                qt.QLabel('Achievements:  '),
                qt.QLabel(case[53])
            )
            md_form.addRow(
                qt.QLabel('During Holidays:  '),
                qt.QLabel(case[54])
            )

            md_grp.setLayout(md_form)
            vbox.addWidget(md_grp)

            # Current Medications
            cm_grp = qt.QGroupBox('Current Medications')
            cm_form = qt.QFormLayout()

            cm_form.addRow(
                qt.QLabel('Current Medications:  '),
                qt.QLabel(case[61])
            )

            cm_grp.setLayout(cm_form)
            vbox.addWidget(cm_grp)

            # Accutes
            at_grp = qt.QGroupBox('Accutes')
            at_form = qt.QFormLayout()

            at_form.addRow(
                qt.QLabel('Accutes:  '),
                qt.QLabel(case[62])
            )

            at_grp.setLayout(at_form)
            vbox.addWidget(at_grp)

            # Final Prescription
            fp_grp = qt.QGroupBox('Final Prescription')
            fp_form = qt.QFormLayout()

            fp_form.addRow(
                qt.QLabel('Totality:  '),
                qt.QLabel(case[63])
            )
            fp_form.addRow(
                qt.QLabel('Rubrics:  '),
                qt.QLabel(case[64])
            )
            fp_form.addRow(
                qt.QLabel('Prescription + Potency:  '),
                qt.QLabel(case[65])
            )
            fp_form.addRow(
                qt.QLabel('D/D:  '),
                qt.QLabel(case[70])
            )

            fp_grp.setLayout(fp_form)
            vbox.addWidget(fp_grp)

        else:
            vbox.addWidget(qt.QLabel('No Case for this Patient'))

        # Set Scrolling Layout
        scroll_widget.setLayout(vbox)
        scroll_win.setWidget(scroll_widget)
        scroll_layout.addWidget(scroll_win)
        self.setLayout(scroll_layout)

        self.setWindowTitle(patient[1] + ' ' + patient[2])

        # Show Window
        self.setModal(True)
        self.setWindowIcon(settings["icon"])
        self.showMaximized()
        self.exec()
