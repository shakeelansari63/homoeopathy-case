#---------- code:utf8 --------------#
import sqlite3 as sqldb
from .setting import settings
from datetime import datetime


class SQLDB:
    """ Class for Connecting SQL Database"""

    def __init__(self):
        self.dbfile = settings["sqlite_db_file"]

    def run_sql(self, sql):
        try:
            conn = sqldb.connect(self.dbfile)
            curr = conn.cursor()
            curr.execute(sql)
            rows = curr.fetchall()
        except Exception as e:
            print(e)
            rows = []
        finally:
            conn.commit()
            curr.close()
            conn.close()
        return rows

    def create_table(self):
        pass

    def drop_table(self):
        pass

    def reset_all(self):
        try:
            self.drop_table()
        except:
            pass
        finally:
            self.create_table()


class PatientDB(SQLDB):
    """ Patients Database """

    def __init__(self):
        super().__init__()

    def create_table(self):
        sql = """CREATE TABLE IF NOT EXISTS PATIENTS (
              PATIENT_ID BIGINT NOT NULL PRIMARY KEY
            , PATIENT_FIRST_NAME TEXT NOT NULL
            , PATIENT_LAST_NAME TEXT NOT NULL
            , YEAR_OF_BIRTH INTEGER
            , GENDER TEXT
            , PHONE TEXT
            , ADDRESS TEXT
            , OCCUPATION TEXT
            , MARITAL_STATUS TEXT
            , REFERENCED_BY TEXT
            , CREATE_DATE DATETIME)"""

        self.run_sql(sql)

    def drop_table(self):
        sql = """DROP TABLE PATIENTS"""

        self.run_sql(sql)

    def addPatient(self, fname, lname, yob, gender, phone, address, occupation, marstat, refby):
        if not self.check_patient(fname, lname, yob, gender, phone):
            # Create patient ID
            pid = self.get_max_patients() + 1

            # Generate SQL for inserting patient
            sql = """INSERT INTO PATIENTS VALUES
            ({pid}, '{fname}', '{lname}', {yob}, '{gender}', '{phone}'
            , '{address}', '{occupation}', '{marstat}', '{refby}', '{ts}')
            """.format(
                pid=pid, fname=fname, lname=lname, yob=yob, gender=gender, phone=phone, address=address,
                occupation=occupation, marstat=marstat, refby=refby, ts=datetime.now()
            )

            self.run_sql(sql)

            if self.get_patient_by_id(pid):
                return pid
            else:
                return 'NOT ADDED'
        else:
            return 'ALREADY EXIST'

    def updPatient(self, patnid, fname, lname, yob, gender, phone, address, occupation, marstat, refby):
        sql = """UPDATE PATIENTS
        SET PATIENT_FIRST_NAME = '{fname}'
        ,   PATIENT_LAST_NAME = '{lname}'
        ,   YEAR_OF_BIRTH = '{yob}'
        ,   GENDER = '{gender}'
        ,   PHONE = '{phone}'
        ,   ADDRESS = '{address}'
        ,   OCCUPATION = '{occupation}'
        ,   MARITAL_STATUS = '{marstat}'
        ,   REFERENCED_BY = '{refby}'
        WHERE PATIENT_ID = {pid}
        """.format(pid=patnid, fname=fname, lname=lname, yob=yob, gender=gender, phone=phone, address=address,
                   occupation=occupation, marstat=marstat, refby=refby)

        self.run_sql(sql)

    def check_patient(self, fname, lname, yob, gender, phone):
        sql = """SELECT 1 FROM PATIENTS
            WHERE PATIENT_FIRST_NAME = '{fname}'
            AND PATIENT_LAST_NAME = '{lname}'
            AND YEAR_OF_BIRTH = {yob}
            AND GENDER = '{gender}'
            AND PHONE = '{phone}'""".format(fname=fname, lname=lname, yob=yob, gender=gender, phone=phone)

        patient_exists = self.run_sql(sql)

        return bool(patient_exists)

    def get_max_patients(self):
        sql = """SELECT COALESCE(MAX(PATIENT_ID), 0) FROM PATIENTS"""
        row = self.run_sql(sql)

        return row[0][0]

    def get_patient_by_id(self, patient_id):
        sql = """SELECT * FROM PATIENTS
            WHERE PATIENT_ID = {patient_id}""".format(patient_id=patient_id)

        patient = self.run_sql(sql)

        return patient[0]

    def get_top_20_patients(self):
        sql = """SELECT * FROM PATIENTS
            ORDER BY CREATE_DATE DESC
            LIMIT 20"""

        rows = self.run_sql(sql)

        return rows

    def search_patient(self, key):
        sql = """SELECT * FROM PATIENTS
            WHERE TRIM(PATIENT_FIRST_NAME) || ' ' || TRIM(PATIENT_LAST_NAME) || ' ' || TRIM(ADDRESS) LIKE '%{}%'
            ORDER BY CREATE_DATE DESC
            LIMIT 20""".format(key.upper())

        rows = self.run_sql(sql)

        return rows

    def search_patient_by_id(self, pid):
        sql = """SELECT * FROM PATIENTS
            WHERE TRIM(PATIENT_ID) LIKE '{}%'
            ORDER BY CREATE_DATE DESC
            LIMIT 20""".format(pid)

        rows = self.run_sql(sql)

        return rows


class CaseDB(SQLDB):
    """ Case DB """

    def __init__(self):
        super().__init__()

    def create_table(self):
        sql = """CREATE TABLE IF NOT EXISTS CASES (
              CASE_ID BIGINT NOT NULL PRIMARY KEY
            , PATIENT_ID BIGINT NOT NULL
            , CC_LOCATION TEXT
            , CC_SENSATION TEXT
            , CC_AGGRAVATION TEXT
            , CC_AMELIORATION TEXT
            , CC_CONCOMETENT TEXT
            , CC_ALLOPATHY_MED TEXT
            , AC_LOCATIONS TEXT
            , AC_SENSATIONS TEXT
            , AC_AGGRAVATION TEXT
            , AC_AMELIORATIONS TEXT
            , AC_CONCOMETENTS TEXT
            , AC_ALLOPATHY_MED TEXT
            , PAST_HISTORY TEXT
            , MENSTRUAL_HISTORY TEXT
            , LEUCORRHOEA TEXT
            , GYNAEC_HISTORY TEXT
            , APPETITE TEXT
            , THERMAL TEXT
            , THIRST TEXT
            , AVERSION TEXT
            , DISAGREE TEXT
            , UNDIGESTABLE TEXT
            , HUNGER TEXT
            , STOOL TEXT
            , URINE TEXT
            , SWEAT TEXT
            , SLEEP TEXT
            , DREAMS TEXT
            , SKIN TEXT
            , NAILS TEXT
            , HOBBIES TEXT
            , ADDICTION TEXT
            , SMELL TEXT
            , TASTE TEXT
            , TOUCH TEXT
            , VISION TEXT
            , HEARING TEXT
            , FAMILY_HISTORY TEXT
            , MIND_DISPOSITION TEXT
            , TEETHING TEXT
            , CRAWLING TEXT
            , WALKING TEXT
            , SPEAKING TEXT
            , VACCINE TEXT
            , HEAD_CROWN TEXT
            , CURRENT_MED TEXT
            , ACCUTES TEXT
            , TOTALITY TEXT
            , RUBRICS TEXT
            , PRESCRIPTION TEXT
            , UPDATE_DATE DATETIME
            , DESIRE TEXT
            , TONGUE TEXT
            , SPEED TEXT
            , ENERGY TEXT
            , DD TEXT
            , SUN TEXT
            )"""

        self.run_sql(sql)

    def drop_table(self):
        sql = """DROP TABLE CASES"""

        self.run_sql(sql)

    def get_max_caseid(self):
        sql = """SELECT COALESCE(MAX(CASE_ID), 0) FROM CASES"""
        row = self.run_sql(sql)

        return row[0][0]

    def save_case(self,
                  pid,
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
                  md_all,
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
                  pg_sun=''):
        """ Save case to Database """
        new_case_id = self.get_max_caseid() + 1

        sql = """INSERT INTO CASES (
              CASE_ID
            , PATIENT_ID
            , CC_LOCATION
            , CC_SENSATION
            , CC_AGGRAVATION
            , CC_AMELIORATION
            , CC_CONCOMETENT
            , CC_ALLOPATHY_MED
            , AC_LOCATIONS
            , AC_SENSATIONS
            , AC_AGGRAVATION
            , AC_AMELIORATIONS
            , AC_CONCOMETENTS
            , AC_ALLOPATHY_MED
            , PAST_HISTORY
            , MENSTRUAL_HISTORY
            , LEUCORRHOEA
            , GYNAEC_HISTORY
            , APPETITE
            , THERMAL
            , THIRST
            , AVERSION
            , DISAGREE
            , UNDIGESTABLE
            , HUNGER
            , STOOL
            , URINE
            , SWEAT
            , SLEEP
            , DREAMS
            , SKIN
            , NAILS
            , HOBBIES
            , ADDICTION
            , SMELL
            , TASTE
            , TOUCH
            , VISION
            , HEARING
            , FAMILY_HISTORY
            , MIND_DISPOSITION
            , TEETHING
            , CRAWLING
            , WALKING
            , SPEAKING
            , VACCINE
            , HEAD_CROWN
            , CURRENT_MED
            , ACCUTES
            , TOTALITY
            , RUBRICS
            , PRESCRIPTION
            , UPDATE_DATE
            , DESIRE
            , TONGUE
            , SPEED
            , ENERGY
            , DD
            , SUN
        ) VALUES (
             {} ,
             {} ,
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}',
            '{}'
        )""".format(
            new_case_id,
            pid,
            cc_loc,
            cc_sen,
            cc_agg,
            cc_ame,
            cc_con,
            cc_alp,
            ac_loc,
            ac_sen,
            ac_agg,
            ac_ame,
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
            md_all,
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
            datetime.now(),
            pg_des,
            pg_ton,
            pg_spd,
            pg_eng,
            fp_dds,
            pg_sun
        )

        self.run_sql(sql)

        self.delete_old_cases(pid, new_case_id)

        return new_case_id

    def get_case_by_patient(self, patient_id):
        sql = """SELECT 
              CC_LOCATION
            , CC_SENSATION
            , CC_AGGRAVATION
            , CC_AMELIORATION
            , CC_CONCOMETENT
            , CC_ALLOPATHY_MED
            , AC_LOCATIONS
            , AC_SENSATIONS
            , AC_AGGRAVATION
            , AC_AMELIORATIONS
            , AC_CONCOMETENTS
            , AC_ALLOPATHY_MED
            , PAST_HISTORY
            , MENSTRUAL_HISTORY
            , LEUCORRHOEA
            , GYNAEC_HISTORY
            , APPETITE
            , THERMAL
            , THIRST
            , AVERSION
            , DISAGREE
            , UNDIGESTABLE
            , HUNGER
            , STOOL
            , URINE
            , SWEAT
            , SLEEP
            , DREAMS
            , SKIN
            , NAILS
            , HOBBIES
            , ADDICTION
            , SMELL
            , TASTE
            , TOUCH
            , VISION
            , HEARING
            , FAMILY_HISTORY
            , MIND_DISPOSITION
            , TEETHING
            , CRAWLING
            , WALKING
            , SPEAKING
            , VACCINE
            , HEAD_CROWN
            , CURRENT_MED
            , ACCUTES
            , TOTALITY
            , RUBRICS
            , PRESCRIPTION
            , DESIRE
            , TONGUE
            , SPEED
            , ENERGY
            , DD
            , SUN
            FROM CASES WHERE PATIENT_ID = {pid}
            AND CASE_ID = ( SELECT MAX(CASE_ID) FROM CASES 
            WHERE PATIENT_ID = {pid})""".format(pid=patient_id)

        case = self.run_sql(sql)

        if case:
            return case[0]
        else:
            return None

    def get_case_by_id(self, case_id):
        sql = """SELECT 
              CC_LOCATION
            , CC_SENSATION
            , CC_AGGRAVATION
            , CC_AMELIORATION
            , CC_CONCOMETENT
            , CC_ALLOPATHY_MED
            , AC_LOCATIONS
            , AC_SENSATIONS
            , AC_AGGRAVATION
            , AC_AMELIORATIONS
            , AC_CONCOMETENTS
            , AC_ALLOPATHY_MED
            , PAST_HISTORY
            , MENSTRUAL_HISTORY
            , LEUCORRHOEA
            , GYNAEC_HISTORY
            , APPETITE
            , THERMAL
            , THIRST
            , AVERSION
            , DISAGREE
            , UNDIGESTABLE
            , HUNGER
            , STOOL
            , URINE
            , SWEAT
            , SLEEP
            , DREAMS
            , SKIN
            , NAILS
            , HOBBIES
            , ADDICTION
            , SMELL
            , TASTE
            , TOUCH
            , VISION
            , HEARING
            , FAMILY_HISTORY
            , MIND_DISPOSITION
            , TEETHING
            , CRAWLING
            , WALKING
            , SPEAKING
            , VACCINE
            , HEAD_CROWN
            , CURRENT_MED
            , ACCUTES
            , TOTALITY
            , RUBRICS
            , PRESCRIPTION
            , DESIRE
            , TONGUE
            , SPEED
            , ENERGY
            , DD
            , SUN
            FROM CASES WHERE CASE_ID = {cid}""".format(cid=case_id)

        case = self.run_sql(sql)

        if case:
            return case[0]
        else:
            return None

    def delete_old_cases(self, pid, new_case_id):
        cases = self.get_cases_of_patient(pid)

        for case in cases:
            if case:
                caseid = case[0]
                if caseid != new_case_id:
                    self.delete_case(caseid)

    def get_cases_of_patient(self, pid):
        sql = """
        SELECT CASE_ID FROM CASES
        WHERE PATIENT_ID = {}
        """.format(pid)

        return self.run_sql(sql)

    def delete_case(self, caseid):
        sql = """
        DELETE FROM CASES
        WHERE CASE_ID = {}
        """.format(caseid)

        self.run_sql(sql)

    def upgrade_db(self):
        sqls = ["""ALTER TABLE CASES
        ADD COLUMN SUN TEXT;""", 
        """ALTER TABLE CASES
        ADD COLUMN MIND_DISPOSITION TEXT;"""]

        retrn_code = 0

        for sql in sqls:
            try:
                self.run_sql(sql)
            except Exception as e:
                retrn_code = 1
                print(e)
        
        return retrn_code
