import { createReducer, on } from "@ngrx/store";

// Initial State for Reducer
import { initialState } from "./patient.state";
// Actions for Reducer
import {
    addPatient,
    replacePatientList,
    displayNewPatientForm,
    hideNewPatientForm
} from './patient.actions'
import { state } from "@angular/animations";

export const patientReducer = createReducer(
    // Initial State
    initialState,

    // Reducer for Replace Patients List action
    on(replacePatientList, (state, action) => {
        return {
            ...state,
            patientsList: action.patientList
        }
    }),

    // Reducer for Add patient
    on(addPatient, (state, action) => {
        return {
            ...state,
            patientsList: [action.patient, ...state.patientsList]
        }
    }),

    // Reducer for Showing Patient Form
    on(displayNewPatientForm, state => {
        return {
            ...state,
            newFormVisibe: true
        }
    }),

    // Reducer for Hiding Patient Form
    on(hideNewPatientForm, state => {
        return {
            ...state,
            newFormVisibe: false
        }
    })
);