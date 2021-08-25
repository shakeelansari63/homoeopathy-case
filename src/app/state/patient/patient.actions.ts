import { createAction, props } from "@ngrx/store";
import { Patient } from '../../models/patient'

const createPatient = createAction('[PATIENT LIST] Add New Patient', props<Patient>)