import { Component, OnInit, OnDestroy } from '@angular/core';
import { PatientsDataService } from '../../services/patients-data.service';
import { Patient } from '../../models/patient';
import { Store } from '@ngrx/store';
// Selectors
import { 
  patientsList,
  newFormView
 } from '../../state/patient/patient.selector';
// Actions
import {
  displayNewPatientForm
} from '../../state/patient/patient.actions'
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-patients',
  templateUrl: './patients.component.html',
  styleUrls: ['./patients.component.scss']
})
export class PatientsComponent implements OnInit, OnDestroy {

  constructor(private pat: PatientsDataService, private store: Store) { }

  searchKey: string='';
  newPatientFormVisible: boolean = false;
  patients: Patient[];
  patListSub: Subscription;
  newPatVisibleSub: Subscription;

  ngOnInit(): void {
    this.pat.getAllPatients()

    // Subscribe to Store patient list
    this.patListSub = this.store.select(patientsList).subscribe( pats => {
      this.patients = pats;
    })

    // Subscribe to New Patients Visible Store component
    this.newPatVisibleSub = this.store.select(newFormView).subscribe(visible => {
      this.newPatientFormVisible = visible;
    })
  }

  ngOnDestroy(): void {
    this.patListSub.unsubscribe();
    this.newPatVisibleSub.unsubscribe();
  }

  searchPatient() {
    console.log(this.searchKey)
  }

  newPatient() {
    console.log('Creating new patient')
    this.store.dispatch(displayNewPatientForm());
  }
}
