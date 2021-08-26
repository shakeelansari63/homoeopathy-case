import { createFeatureSelector, createSelector } from '@ngrx/store';
import { PatientState } from '../../models/patient'

const patientsFeatureSelector = createFeatureSelector<PatientState>('patients');

export const patientsList = createSelector(patientsFeatureSelector, state => state.patientsList)
export const newFormView = createSelector(patientsFeatureSelector, state => state.newFormVisibe)