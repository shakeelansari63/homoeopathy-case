from PyQt5 import QtWidgets as qt
from PyQt5 import QtGui as gui
from PyQt5 import QtCore as core
from .db import PatientDB, CaseDB
from .alert import MsgErrBox, MsgSucBox
from .setting import settings
from datetime import date
from functools import partial


class Case(qt.QDialog):
    """ Create New case """

    def __init__(self):
        super().__init__()

        # Db Connection
        self.sqldb = PatientDB()
        self.casedb = CaseDB()

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
        ccform = qt.QHBoxLayout()
        # Complaint Location
        self.cc_location = qt.QTextEdit()
        self.cc_location.setPlaceholderText('Location')
        self.cc_location.setTabChangesFocus(True)
        cc_loc_col = qt.QVBoxLayout()
        cc_loc_col.addWidget(qt.QLabel('Location'))
        cc_loc_col.addWidget(self.cc_location)
        cc_loc_col.setAlignment(core.Qt.AlignTop)
        ccform.addLayout(cc_loc_col)
        # Complaint Sensation
        self.cc_sensation = qt.QTextEdit()
        self.cc_sensation.setPlaceholderText('Sensation')
        self.cc_sensation.setTabChangesFocus(True)
        cc_sen_col = qt.QVBoxLayout()
        cc_sen_col.addWidget(qt.QLabel('Sensation'))
        cc_sen_col.addWidget(self.cc_sensation)
        cc_sen_col.setAlignment(core.Qt.AlignTop)
        ccform.addLayout(cc_sen_col)
        # Modality
        self.cc_amelioration = qt.QTextEdit()
        self.cc_amelioration.setPlaceholderText('Amelioration')
        self.cc_amelioration.setTabChangesFocus(True)
        self.cc_aggrevation = qt.QTextEdit()
        self.cc_aggrevation.setPlaceholderText('Aggrevation')
        self.cc_aggrevation.setTabChangesFocus(True)
        cc_mod_col = qt.QVBoxLayout()
        cc_mod_col.addWidget(qt.QLabel('Modality'))
        cc_mod_col.addWidget(self.cc_amelioration)
        cc_mod_col.addWidget(self.cc_aggrevation)
        cc_mod_col.setAlignment(core.Qt.AlignTop)
        ccform.addLayout(cc_mod_col)
        # Concometent
        self.cc_concometent = qt.QTextEdit()
        self.cc_concometent.setPlaceholderText('Concomitant')
        self.cc_concometent.setTabChangesFocus(True)
        cc_conc_col = qt.QVBoxLayout()
        cc_conc_col.addWidget(qt.QLabel('Concomitant'))
        cc_conc_col.addWidget(self.cc_concometent)
        cc_conc_col.setAlignment(core.Qt.AlignTop)
        ccform.addLayout(cc_conc_col)
        # Add form to Group
        chief_complaint_grp.setLayout(ccform)
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
        self.past_hist = qt.QTextEdit()
        self.past_hist.setPlaceholderText('Past History')
        self.past_hist.setTabChangesFocus(True)
        phvbox.addWidget(self.past_hist)
        # Add form to Group
        past_history_grp.setLayout(phvbox)
        # Add Group to Vbox
        self.vbox.addWidget(past_history_grp)

        # Female Specific
        # Menstrual History
        self.mens_hist = qt.QTextEdit()
        self.mens_hist.setPlaceholderText('Menstrual History')
        self.mens_hist.setTabChangesFocus(True)
        # Leucorrhoea
        self.leucorrhoea = qt.QTextEdit()
        self.leucorrhoea.setPlaceholderText('Leucorrhoea')
        self.leucorrhoea.setTabChangesFocus(True)
        # Gyenac History
        self.gynaec_hist = qt.QTextEdit()
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
        self.ch_teething = qt.QTextEdit()
        self.ch_teething.setPlaceholderText('Teething')
        self.ch_teething.setTabChangesFocus(True)
        # Crawling
        self.ch_crawling = qt.QTextEdit()
        self.ch_crawling.setPlaceholderText('Crawling')
        self.ch_crawling.setTabChangesFocus(True)
        # Walking
        self.ch_walking = qt.QTextEdit()
        self.ch_walking.setPlaceholderText('Walking')
        self.ch_walking.setTabChangesFocus(True)
        # Speaking
        self.ch_speaking = qt.QTextEdit()
        self.ch_speaking.setPlaceholderText('Speaking')
        self.ch_speaking.setTabChangesFocus(True)
        # Vaccine
        self.ch_vaccine = qt.QTextEdit()
        self.ch_vaccine.setPlaceholderText('Vaccine')
        self.ch_vaccine.setTabChangesFocus(True)
        # Head and Crown
        self.ch_headcrown = qt.QTextEdit()
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
        # Appetite
        self.pg_appetite = qt.QTextEdit()
        self.pg_appetite.setPlaceholderText('Appetite')
        self.pg_appetite.setTabChangesFocus(True)
        pgform.addRow(qt.QLabel('Appetite:  '), self.pg_appetite)
        # Thermals
        self.pg_thermal = qt.QTextEdit()
        self.pg_thermal.setPlaceholderText('Thermals')
        self.pg_thermal.setTabChangesFocus(True)
        pgform.addRow(qt.QLabel('Thermals:  '), self.pg_thermal)
        # Thurst
        self.pg_thurst = qt.QTextEdit()
        self.pg_thurst.setPlaceholderText('Thurst')
        self.pg_thurst.setTabChangesFocus(True)
        pgform.addRow(qt.QLabel('Thurst:  '), self.pg_thurst)
        # Aversion
        self.pg_aversion = qt.QTextEdit()
        self.pg_aversion.setPlaceholderText('Aversion')
        self.pg_aversion.setTabChangesFocus(True)
        pgform.addRow(qt.QLabel('Aversion:  '), self.pg_aversion)
        # Disagree
        self.pg_disagree = qt.QTextEdit()
        self.pg_disagree.setPlaceholderText('Disagree')
        self.pg_disagree.setTabChangesFocus(True)
        pgform.addRow(qt.QLabel('Disagree:  '), self.pg_disagree)
        # Undigestable Things
        self.pg_undigestable = qt.QTextEdit()
        self.pg_undigestable.setPlaceholderText('Undigestable Things')
        self.pg_undigestable.setTabChangesFocus(True)
        pgform.addRow(qt.QLabel('Undigestable Things:  '),
                      self.pg_undigestable)
        # Hunger
        self.pg_hunger = qt.QTextEdit()
        self.pg_hunger.setPlaceholderText('Hunger')
        self.pg_hunger.setTabChangesFocus(True)
        pgform.addRow(qt.QLabel('Hunger:  '), self.pg_hunger)
        # Stool
        self.pg_stool = qt.QTextEdit()
        self.pg_stool.setPlaceholderText('Stool')
        self.pg_stool.setTabChangesFocus(True)
        pgform.addRow(qt.QLabel('Stool:  '), self.pg_stool)
        # Urine
        self.pg_urine = qt.QTextEdit()
        self.pg_urine.setPlaceholderText('Urine')
        self.pg_urine.setTabChangesFocus(True)
        pgform.addRow(qt.QLabel('Urine:  '), self.pg_urine)
        # Sweat
        self.pg_sweat = qt.QTextEdit()
        self.pg_sweat.setPlaceholderText('Sweat')
        self.pg_sweat.setTabChangesFocus(True)
        pgform.addRow(qt.QLabel('Sweat:  '), self.pg_sweat)
        # Sleep
        self.pg_sleep = qt.QTextEdit()
        self.pg_sleep.setPlaceholderText('Sleep')
        self.pg_sleep.setTabChangesFocus(True)
        pgform.addRow(qt.QLabel('Sleep:  '), self.pg_sleep)
        # Dreams
        self.pg_dreams = qt.QTextEdit()
        self.pg_dreams.setPlaceholderText('Dreams')
        self.pg_dreams.setTabChangesFocus(True)
        pgform.addRow(qt.QLabel('Dreams:  '), self.pg_dreams)
        # Skin
        self.pg_skin = qt.QTextEdit()
        self.pg_skin.setPlaceholderText('Skin')
        self.pg_skin.setTabChangesFocus(True)
        pgform.addRow(qt.QLabel('Skin:  '), self.pg_skin)
        # Nails
        self.pg_nails = qt.QTextEdit()
        self.pg_nails.setPlaceholderText('Nails')
        self.pg_nails.setTabChangesFocus(True)
        pgform.addRow(qt.QLabel('Nails:  '), self.pg_nails)
        # Hobbies
        self.pg_hobbies = qt.QTextEdit()
        self.pg_hobbies.setPlaceholderText('Hobbies')
        self.pg_hobbies.setTabChangesFocus(True)
        pgform.addRow(qt.QLabel('Hobbies:  '), self.pg_hobbies)
        # Addiction
        self.pg_addiction = qt.QTextEdit()
        self.pg_addiction.setPlaceholderText('Addiction')
        self.pg_addiction.setTabChangesFocus(True)
        pgform.addRow(qt.QLabel('Addiction:  '), self.pg_addiction)
        # Sensitivity
        snsrow = qt.QHBoxLayout()
        # Smell
        self.pg_smell = qt.QTextEdit()
        self.pg_smell.setPlaceholderText('Smell')
        self.pg_smell.setTabChangesFocus(True)
        snsrow.addWidget(self.pg_smell)
        # Taste
        self.pg_taste = qt.QTextEdit()
        self.pg_taste.setPlaceholderText('Taste')
        self.pg_taste.setTabChangesFocus(True)
        snsrow.addWidget(self.pg_taste)
        # Touch
        self.pg_touch = qt.QTextEdit()
        self.pg_touch.setPlaceholderText('Touch')
        self.pg_touch.setTabChangesFocus(True)
        snsrow.addWidget(self.pg_touch)
        # Vision
        self.pg_vision = qt.QTextEdit()
        self.pg_vision.setPlaceholderText('Vision')
        self.pg_vision.setTabChangesFocus(True)
        snsrow.addWidget(self.pg_vision)
        # Hearning
        self.pg_hearing = qt.QTextEdit()
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
        self.fam_hist = qt.QTextEdit()
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
        self.md_childhood = qt.QTextEdit()
        self.md_childhood.setPlaceholderText('Childhood')
        self.md_childhood.setTabChangesFocus(True)
        mdform.addRow(qt.QLabel('Childhood:  '), self.md_childhood)
        # Education
        self.md_education = qt.QTextEdit()
        self.md_education.setPlaceholderText('Education')
        self.md_education.setTabChangesFocus(True)
        mdform.addRow(qt.QLabel('Education:  '), self.md_education)
        # Marriage
        self.md_marriage = qt.QTextEdit()
        self.md_marriage.setPlaceholderText('Marriage')
        self.md_marriage.setTabChangesFocus(True)
        mdform.addRow(qt.QLabel('Marriage:  '), self.md_marriage)
        # Children
        self.md_children = qt.QTextEdit()
        self.md_children.setPlaceholderText('Children')
        self.md_children.setTabChangesFocus(True)
        mdform.addRow(qt.QLabel('Children:  '), self.md_children)
        # Expenses
        self.md_expenses = qt.QTextEdit()
        self.md_expenses.setPlaceholderText('Expenses')
        self.md_expenses.setTabChangesFocus(True)
        mdform.addRow(qt.QLabel('Expenses:  '), self.md_expenses)
        # Religiousness
        self.md_religious = qt.QTextEdit()
        self.md_religious.setPlaceholderText('Religiousness')
        self.md_religious.setTabChangesFocus(True)
        mdform.addRow(qt.QLabel('Religiousness:  '), self.md_religious)
        # Cleanliness
        self.md_cleanliness = qt.QTextEdit()
        self.md_cleanliness.setPlaceholderText('Cleanliness')
        self.md_cleanliness.setTabChangesFocus(True)
        mdform.addRow(qt.QLabel('Cleanliness:  '), self.md_cleanliness)
        # Sympathy
        self.md_sympathy = qt.QTextEdit()
        self.md_sympathy.setPlaceholderText('Sympathy')
        self.md_sympathy.setTabChangesFocus(True)
        mdform.addRow(qt.QLabel('Sympathy:  '), self.md_sympathy)
        # Anger
        self.md_anger = qt.QTextEdit()
        self.md_anger.setPlaceholderText('Anger')
        self.md_anger.setTabChangesFocus(True)
        mdform.addRow(qt.QLabel('Anger:  '), self.md_anger)
        # Destruction
        self.md_destruction = qt.QTextEdit()
        self.md_destruction.setPlaceholderText('Destruction')
        self.md_destruction.setTabChangesFocus(True)
        mdform.addRow(qt.QLabel('Destruction:  '), self.md_destruction)
        # Sexual History
        self.md_sexualhist = qt.QTextEdit()
        self.md_sexualhist.setPlaceholderText('Sexual History')
        self.md_sexualhist.setTabChangesFocus(True)
        mdform.addRow(qt.QLabel('Sexual History:  '), self.md_sexualhist)
        # Future Plans
        self.md_futureplans = qt.QTextEdit()
        self.md_futureplans.setPlaceholderText('Future Plans')
        self.md_futureplans.setTabChangesFocus(True)
        mdform.addRow(qt.QLabel('Future Plans:  '), self.md_futureplans)
        # Business
        self.md_business = qt.QTextEdit()
        self.md_business.setPlaceholderText('Business')
        self.md_business.setTabChangesFocus(True)
        mdform.addRow(qt.QLabel('Business:  '), self.md_business)
        # Weeping
        self.md_weeping = qt.QTextEdit()
        self.md_weeping.setPlaceholderText('Weeping')
        self.md_weeping.setTabChangesFocus(True)
        mdform.addRow(qt.QLabel('Weeping:  '), self.md_weeping)
        # During Illness
        self.md_illness = qt.QTextEdit()
        self.md_illness.setPlaceholderText('During Illness')
        self.md_illness.setTabChangesFocus(True)
        mdform.addRow(qt.QLabel('During Illness:  '), self.md_illness)
        # Achievements
        self.md_achievements = qt.QTextEdit()
        self.md_achievements.setPlaceholderText('Achievements')
        self.md_achievements.setTabChangesFocus(True)
        mdform.addRow(qt.QLabel('Achievements:  '), self.md_achievements)
        # During Holidays
        self.md_holidays = qt.QTextEdit()
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
        self.cur_med = qt.QTextEdit()
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
        self.accute = qt.QTextEdit()
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
        self.fp_totality = qt.QTextEdit()
        self.fp_totality.setPlaceholderText('Totality')
        self.fp_totality.setTabChangesFocus(True)
        fpform.addRow(qt.QLabel('Totality:  '), self.fp_totality)
        # Rubrics
        self.fp_rubrics = qt.QTextEdit()
        self.fp_rubrics.setPlaceholderText('Rubrics')
        self.fp_rubrics.setTabChangesFocus(True)
        fpform.addRow(qt.QLabel('Rubrics:  '), self.fp_rubrics)
        # Prescription + Potency
        pp_row = qt.QHBoxLayout()
        self.fp_prescription = qt.QTextEdit()
        self.fp_prescription.setPlaceholderText('Prescription')
        self.fp_prescription.setTabChangesFocus(True)
        pp_row.addWidget(self.fp_prescription)
        self.fp_potency = qt.QTextEdit()
        self.fp_potency.setPlaceholderText('Potency')
        self.fp_potency.setTabChangesFocus(True)
        pp_row.addWidget(self.fp_potency)
        fpform.addRow(qt.QLabel('Prescription + Potency:  '), pp_row)
        # Add form to Group
        final_prescription_grp.setLayout(fpform)
        # Add Group to Vbox
        self.vbox.addWidget(final_prescription_grp)

        # Button to save Case
        submit_row = qt.QHBoxLayout()
        save = qt.QPushButton('Save')
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
        self.exec()

    def populate_case(self):
        patient_case = self.casedb.get_case_by_patient(self.pid)

        if patient_case:
            self.cc_location.setPlainText(patient_case[0])
            self.cc_sensation.setPlainText(patient_case[1])
            self.cc_amelioration.setPlainText(patient_case[2])
            self.cc_aggrevation.setPlainText(patient_case[3])
            self.cc_concometent.setPlainText(patient_case[4])
            self.past_hist.setPlainText(patient_case[10])
            self.mens_hist.setPlainText(patient_case[11])
            self.leucorrhoea.setPlainText(patient_case[12])
            self.gynaec_hist.setPlainText(patient_case[13])
            self.pg_appetite.setPlainText(patient_case[14])
            self.pg_thermal.setPlainText(patient_case[15])
            self.pg_thurst.setPlainText(patient_case[16])
            self.pg_aversion.setPlainText(patient_case[17])
            self.pg_disagree.setPlainText(patient_case[18])
            self.pg_undigestable.setPlainText(patient_case[19])
            self.pg_hunger.setPlainText(patient_case[20])
            self.pg_stool.setPlainText(patient_case[21])
            self.pg_urine.setPlainText(patient_case[22])
            self.pg_sweat.setPlainText(patient_case[23])
            self.pg_sleep.setPlainText(patient_case[24])
            self.pg_dreams.setPlainText(patient_case[25])
            self.pg_skin.setPlainText(patient_case[26])
            self.pg_nails.setPlainText(patient_case[27])
            self.pg_hobbies.setPlainText(patient_case[28])
            self.pg_addiction.setPlainText(patient_case[29])
            self.pg_smell.setPlainText(patient_case[30])
            self.pg_taste.setPlainText(patient_case[31])
            self.pg_touch.setPlainText(patient_case[32])
            self.pg_vision.setPlainText(patient_case[33])
            self.pg_hearing.setPlainText(patient_case[34])
            self.fam_hist.setPlainText(patient_case[35])
            self.md_childhood.setPlainText(patient_case[36])
            self.md_education.setPlainText(patient_case[37])
            self.md_marriage.setPlainText(patient_case[38])
            self.md_children.setPlainText(patient_case[39])
            self.md_expenses.setPlainText(patient_case[40])
            self.md_religious.setPlainText(patient_case[41])
            self.md_cleanliness.setPlainText(patient_case[42])
            self.md_sympathy.setPlainText(patient_case[43])
            self.md_anger.setPlainText(patient_case[44])
            self.md_destruction.setPlainText(patient_case[45])
            self.md_sexualhist.setPlainText(patient_case[46])
            self.md_futureplans.setPlainText(patient_case[47])
            self.md_business.setPlainText(patient_case[48])
            self.md_weeping.setPlainText(patient_case[49])
            self.md_illness.setPlainText(patient_case[50])
            self.md_achievements.setPlainText(patient_case[51])
            self.md_holidays.setPlainText(patient_case[52])
            self.ch_teething.setPlainText(patient_case[53])
            self.ch_crawling.setPlainText(patient_case[54])
            self.ch_walking.setPlainText(patient_case[55])
            self.ch_speaking.setPlainText(patient_case[56])
            self.ch_vaccine.setPlainText(patient_case[57])
            self.ch_headcrown.setPlainText(patient_case[58])
            self.cur_med.setPlainText(patient_case[59])
            self.accute.setPlainText(patient_case[60])
            self.fp_totality.setPlainText(patient_case[61])
            self.fp_rubrics.setPlainText(patient_case[62])
            self.fp_prescription.setPlainText(patient_case[63])
            self.fp_potency.setPlainText(patient_case[64])

            # Create associated complaints
            ac_loc = patient_case[5].split('|')
            ac_sen = patient_case[6].split('|')
            ac_ame = patient_case[7].split('|')
            ac_agg = patient_case[8].split('|')
            ac_con = patient_case[9].split('|')
            for asso_compl in zip(ac_loc, ac_sen, ac_ame, ac_agg, ac_con):
                self.add_associated_complaint(*asso_compl)

    def add_associated_complaint(self, ac_loc=None, ac_sen=None, ac_ame=None, ac_agg=None, ac_con=None):
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
        ac_location = qt.QTextEdit()
        ac_location.setPlaceholderText('Location')
        ac_location.setTabChangesFocus(True)
        if ac_loc:
            ac_location.setPlainText(ac_loc)
        ac_loc_col = qt.QVBoxLayout()
        ac_loc_col.addWidget(qt.QLabel('Location'))
        ac_loc_col.addWidget(ac_location)
        ac_loc_col.setAlignment(core.Qt.AlignTop)
        acform.addLayout(ac_loc_col)
        # Complaint Sensation
        ac_sensation = qt.QTextEdit()
        ac_sensation.setPlaceholderText('Sensation')
        ac_sensation.setTabChangesFocus(True)
        if ac_sen:
            ac_sensation.setPlainText(ac_sen)
        ac_sen_col = qt.QVBoxLayout()
        ac_sen_col.addWidget(qt.QLabel('Sensation'))
        ac_sen_col.addWidget(ac_sensation)
        ac_sen_col.setAlignment(core.Qt.AlignTop)
        acform.addLayout(ac_sen_col)
        # Modality
        ac_amelioration = qt.QTextEdit()
        ac_amelioration.setPlaceholderText('Amelioration')
        ac_amelioration.setTabChangesFocus(True)
        if ac_ame:
            ac_amelioration.setPlainText(ac_ame)
        ac_aggrevation = qt.QTextEdit()
        ac_aggrevation.setPlaceholderText('Aggrevation')
        ac_aggrevation.setTabChangesFocus(True)
        if ac_agg:
            ac_aggrevation.setPlainText(ac_agg)
        ac_mod_col = qt.QVBoxLayout()
        ac_mod_col.addWidget(qt.QLabel('Modality'))
        ac_mod_col.addWidget(ac_amelioration)
        ac_mod_col.addWidget(ac_aggrevation)
        ac_mod_col.setAlignment(core.Qt.AlignTop)
        acform.addLayout(ac_mod_col)
        # Concometent
        ac_concometent = qt.QTextEdit()
        ac_concometent.setPlaceholderText('Concomitant')
        ac_concometent.setTabChangesFocus(True)
        if ac_con:
            ac_concometent.setPlainText(ac_con)
        ac_conc_col = qt.QVBoxLayout()
        ac_conc_col.addWidget(qt.QLabel('Concomitant'))
        ac_conc_col.addWidget(ac_concometent)
        ac_conc_col.setAlignment(core.Qt.AlignTop)
        acform.addLayout(ac_conc_col)
        # Add Horizontal form to vertical 1st row
        assoc_vbox.addLayout(acform)
        # Add form to Group
        asso_complaint_grp.setLayout(assoc_vbox)
        # Add Buttons to List
        self.associated_complaint_list[ac_id] = (
            ac_location, ac_sensation, ac_amelioration, ac_aggrevation, ac_concometent)
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
            cc_loc = self.cc_location.toPlainText().replace("'", "''")
            cc_sen = self.cc_sensation.toPlainText().replace("'", "''")
            cc_ame = self.cc_amelioration.toPlainText().replace("'", "''")
            cc_agg = self.cc_aggrevation.toPlainText().replace("'", "''")
            cc_con = self.cc_concometent.toPlainText().replace("'", "''")
            aclitm = self.associated_complaint_list.items()
            # Location in 0th position of value
            ac_loc = "|".join([acl[1][0].toPlainText()
                               for acl in aclitm]).replace("'", "''")
            # Sensation in 1st position of value
            ac_sen = "|".join([acl[1][1].toPlainText()
                               for acl in aclitm]).replace("'", "''")
            # Amelioration in 2nd position of value
            ac_ame = "|".join([acl[1][2].toPlainText()
                               for acl in aclitm]).replace("'", "''")
            # Aggrevation in 3rd position of value
            ac_agg = "|".join([acl[1][3].toPlainText()
                               for acl in aclitm]).replace("'", "''")
            # Concometent in 4th position of value
            ac_con = "|".join([acl[1][4].toPlainText()
                               for acl in aclitm]).replace("'", "''")
            pahist = self.past_hist.toPlainText().replace("'", "''")
            mehist = self.mens_hist.toPlainText().replace("'", "''")
            leucor = self.leucorrhoea.toPlainText().replace("'", "''")
            gynaec = self.gynaec_hist.toPlainText().replace("'", "''")
            pg_app = self.pg_appetite.toPlainText().replace("'", "''")
            pg_the = self.pg_thermal.toPlainText().replace("'", "''")
            pg_thu = self.pg_thurst.toPlainText().replace("'", "''")
            pg_ave = self.pg_aversion.toPlainText().replace("'", "''")
            pg_dis = self.pg_disagree.toPlainText().replace("'", "''")
            pg_und = self.pg_undigestable.toPlainText().replace("'", "''")
            pg_hng = self.pg_hunger.toPlainText().replace("'", "''")
            pg_stl = self.pg_stool.toPlainText().replace("'", "''")
            pg_urn = self.pg_urine.toPlainText().replace("'", "''")
            pg_swt = self.pg_sweat.toPlainText().replace("'", "''")
            pg_slp = self.pg_sleep.toPlainText().replace("'", "''")
            pg_drm = self.pg_dreams.toPlainText().replace("'", "''")
            pg_skn = self.pg_skin.toPlainText().replace("'", "''")
            pg_nls = self.pg_nails.toPlainText().replace("'", "''")
            pg_hbs = self.pg_hobbies.toPlainText().replace("'", "''")
            pg_adc = self.pg_addiction.toPlainText().replace("'", "''")
            pg_sml = self.pg_smell.toPlainText().replace("'", "''")
            pg_tst = self.pg_taste.toPlainText().replace("'", "''")
            pg_tou = self.pg_touch.toPlainText().replace("'", "''")
            pg_vis = self.pg_vision.toPlainText().replace("'", "''")
            pg_hrn = self.pg_hearing.toPlainText().replace("'", "''")
            famhst = self.fam_hist.toPlainText().replace("'", "''")
            md_chd = self.md_childhood.toPlainText().replace("'", "''")
            md_edu = self.md_education.toPlainText().replace("'", "''")
            md_mar = self.md_marriage.toPlainText().replace("'", "''")
            md_crn = self.md_children.toPlainText().replace("'", "''")
            md_exp = self.md_expenses.toPlainText().replace("'", "''")
            md_rlg = self.md_religious.toPlainText().replace("'", "''")
            md_cln = self.md_cleanliness.toPlainText().replace("'", "''")
            md_sym = self.md_sympathy.toPlainText().replace("'", "''")
            md_agr = self.md_anger.toPlainText().replace("'", "''")
            md_dst = self.md_destruction.toPlainText().replace("'", "''")
            md_sxh = self.md_sexualhist.toPlainText().replace("'", "''")
            md_fpl = self.md_futureplans.toPlainText().replace("'", "''")
            md_bsn = self.md_business.toPlainText().replace("'", "''")
            md_wpn = self.md_weeping.toPlainText().replace("'", "''")
            md_ill = self.md_illness.toPlainText().replace("'", "''")
            md_ach = self.md_achievements.toPlainText().replace("'", "''")
            md_hld = self.md_holidays.toPlainText().replace("'", "''")
            ch_tth = self.ch_teething.toPlainText().replace("'", "''")
            ch_crl = self.ch_crawling.toPlainText().replace("'", "''")
            ch_wlk = self.ch_walking.toPlainText().replace("'", "''")
            ch_spk = self.ch_speaking.toPlainText().replace("'", "''")
            ch_vcn = self.ch_vaccine.toPlainText().replace("'", "''")
            ch_hcr = self.ch_headcrown.toPlainText().replace("'", "''")
            curmed = self.cur_med.toPlainText().replace("'", "''")
            accute = self.accute.toPlainText().replace("'", "''")
            fp_ttl = self.fp_totality.toPlainText().replace("'", "''")
            fp_rbr = self.fp_rubrics.toPlainText().replace("'", "''")
            fp_prs = self.fp_prescription.toPlainText().replace("'", "''")
            fp_pot = self.fp_potency.toPlainText().replace("'", "''")

            # Save Case
            case_id = self.casedb.save_case(self.pid,
                                            cc_loc,
                                            cc_sen,
                                            cc_ame,
                                            cc_agg,
                                            cc_con,
                                            ac_loc,
                                            ac_sen,
                                            ac_ame,
                                            ac_agg,
                                            ac_con,
                                            pahist,
                                            mehist,
                                            leucor,
                                            gynaec,
                                            pg_app,
                                            pg_the,
                                            pg_thu,
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
                                            fp_pot)

            case = self.casedb.get_case_by_id(case_id)

            print(case_id)
            print(case)

            if case:
                self.close()
                MsgSucBox('Case Saved Successfully')
            else:
                MsgErrBox('Unable to Save Case')


class ViewCase(qt.QDialog):
    def __init__(self):
        super().__init__()

        # Db Connection
        self.patndb = PatientDB()
        self.casedb = CaseDB()

    def view_case(self, patient_id, case_id=None):
        patient = self.patndb.get_patient_by_id(patient_id)
        if case_id:
            case = self.casedb.get_case_by_id(case_id)
        else:
            case = self.casedb.get_case_by_patient(patient_id)

        # Scroll Widget
        scroll_layout = qt.QVBoxLayout()
        scroll_widget = qt.QWidget()
        scroll_win = qt.QScrollArea()
        vbox = qt.QVBoxLayout()

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

        vbox.addLayout(patnform)

        # Case Information
        # Chief Complaint
        cc_group = qt.QGroupBox('Chief Complaint')
        cc_row = qt.QHBoxLayout()
        cc_loc_group = qt.QGroupBox('Location')
        cc_loc_vbox = qt.QVBoxLayout()
        cc_loc_vbox.addWidget(qt.QLabel(case[0]))
        cc_loc_vbox.setAlignment(core.Qt.AlignTop)
        cc_loc_group.setLayout(cc_loc_vbox)

        cc_sen_group = qt.QGroupBox('Sensation')
        cc_sen_vbox = qt.QVBoxLayout()
        cc_sen_vbox.addWidget(qt.QLabel(case[1]))
        cc_sen_vbox.setAlignment(core.Qt.AlignTop)
        cc_sen_group.setLayout(cc_sen_vbox)

        cc_mod_group = qt.QGroupBox('Modality')
        cc_mod_vbox = qt.QVBoxLayout()
        cc_mod_vbox.addWidget(
            qt.QLabel('Amelioration: \n' + case[2] + '\n\nAggrevation:  \n' + case[3]))
        cc_mod_vbox.setAlignment(core.Qt.AlignTop)
        cc_mod_group.setLayout(cc_mod_vbox)

        cc_con_group = qt.QGroupBox('Concomitant')
        cc_con_vbox = qt.QVBoxLayout()
        cc_con_vbox.addWidget(qt.QLabel(case[4]))
        cc_con_vbox.setAlignment(core.Qt.AlignTop)
        cc_con_group.setLayout(cc_sen_vbox)

        cc_row.addWidget(cc_loc_group)
        # cc_row.addStretch()
        cc_row.addWidget(cc_sen_group)
        # cc_row.addStretch()
        cc_row.addWidget(cc_mod_group)
        # cc_row.addStretch()
        cc_row.addWidget(cc_con_group)
        cc_group.setLayout(cc_row)

        vbox.addWidget(cc_group)

        # Associated Complaint
        ac_group = qt.QGroupBox('Associated Complaints')
        ac_vbox = qt.QVBoxLayout()
        ac_loc = case[5].split('|')
        ac_sen = case[6].split('|')
        ac_ame = case[7].split('|')
        ac_agg = case[8].split('|')
        ac_con = case[9].split('|')
        for ac_loc_data, ac_sen_data, ac_ame_data, ac_agg_data, ac_con_data in zip(ac_loc, ac_sen, ac_ame, ac_agg, ac_con):
            ac_row = qt.QHBoxLayout()
            ac_loc_group = qt.QGroupBox('Location')
            ac_loc_vbox = qt.QVBoxLayout()
            ac_loc_vbox.addWidget(qt.QLabel(ac_loc_data))
            ac_loc_vbox.setAlignment(core.Qt.AlignTop)
            ac_loc_group.setLayout(ac_loc_vbox)

            ac_sen_group = qt.QGroupBox('Sensation')
            ac_sen_vbox = qt.QVBoxLayout()
            ac_sen_vbox.addWidget(qt.QLabel(ac_sen_data))
            ac_sen_vbox.setAlignment(core.Qt.AlignTop)
            ac_sen_group.setLayout(ac_sen_vbox)

            ac_mod_group = qt.QGroupBox('Modality')
            ac_mod_vbox = qt.QVBoxLayout()
            ac_mod_vbox.addWidget(
                qt.QLabel('Amelioration: \n' + ac_ame_data + '\n\nAggrevation:  \n' + ac_agg_data))
            ac_mod_vbox.setAlignment(core.Qt.AlignTop)
            ac_mod_group.setLayout(ac_mod_vbox)

            ac_con_group = qt.QGroupBox('Concomitant')
            ac_con_vbox = qt.QVBoxLayout()
            ac_con_vbox.addWidget(qt.QLabel(ac_con_data))
            ac_con_vbox.setAlignment(core.Qt.AlignTop)
            ac_con_group.setLayout(ac_sen_vbox)

            ac_row.addWidget(ac_loc_group)
            # ac_row.addStretch()
            ac_row.addWidget(ac_sen_group)
            # ac_row.addStretch()
            ac_row.addWidget(ac_mod_group)
            # ac_row.addStretch()
            ac_row.addWidget(ac_con_group)
            ac_vbox.addLayout(ac_row)

        ac_group.setLayout(ac_vbox)
        vbox.addWidget(ac_group)
        # Set Scrolling Layout
        scroll_widget.setLayout(vbox)
        scroll_win.setWidget(scroll_widget)
        scroll_layout.addWidget(scroll_win)
        self.setLayout(scroll_layout)

        self.setWindowTitle(patient[1] + ' ' + patient[2])

        # Show Window
        self.setModal(True)
        self.exec()
