import { createAction, props } from "@ngrx/store";
import { Patient } from '../../models/patient'

export const addPatient = createAction('[PATIENT LIST] Add New Patient', props<{patient: Patient}>());
export const replacePatientList = createAction('[PATIENT LIST] Replace', props<{patientList: Patient[]}>());
export const displayNewPatientForm = createAction('[PATIENT FORM] Show');
export const hideNewPatientForm = createAction('[PATIENT FORM] Hide');