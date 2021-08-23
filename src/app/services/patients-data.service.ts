import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Patient } from '../models/patient'
import { Subject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PatientsDataService {

  baseUrl: string = 'http://localhost:3000'
  patientsUrl: string = `${this.baseUrl}/patients`
  hdr: HttpHeaders = new HttpHeaders({ 'Content-Type': 'application/json'})

  constructor(private http: HttpClient) {
   }

  newPatient(pat: Patient) {
    return this.http.post<Patient>(this.patientsUrl, pat, {headers: this.hdr})
  }

  getAllPatients() : Observable<any> {
    return this.http.get<Patient[]>(this.patientsUrl)
  }
}
