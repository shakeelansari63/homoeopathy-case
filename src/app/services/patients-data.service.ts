import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Patient } from '../models/patient'
import { Store } from '@ngrx/store';
import { 
  addPatient, 
  replacePatientList,
  hideNewPatientForm 
} from '../state/patient/patient.actions'
import { Subject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PatientsDataService {

  baseUrl: string = 'http://localhost:3000'
  patientsUrl: string = `${this.baseUrl}/patients`
  hdr: HttpHeaders = new HttpHeaders({ 'Content-Type': 'application/json'})

  constructor(private http: HttpClient, private store: Store) {
   }

  newPatient(pat: Patient) {
    this.http.post<Patient>(this.patientsUrl, pat, {headers: this.hdr}).forEach( result => {
      this.store.dispatch(hideNewPatientForm())
    })

    this.store.dispatch(addPatient({patient: pat}))
  }

  getAllPatients() {
    this.http.get<Patient[]>(this.patientsUrl).forEach( patients => {
      this.store.dispatch(replacePatientList({patientList: patients}))
    })
  }
}
