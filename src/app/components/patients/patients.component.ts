import { Component, OnInit } from '@angular/core';
import { PatientsDataService } from '../../services/patients-data.service';
import { Patient } from '../../models/patient';

@Component({
  selector: 'app-patients',
  templateUrl: './patients.component.html',
  styleUrls: ['./patients.component.scss']
})
export class PatientsComponent implements OnInit {

  constructor(private pat: PatientsDataService) { }

  searchKey: string='';
  newPatientFormVisible: boolean = false;
  patients: Patient[];

  ngOnInit(): void {
    this.pat.getAllPatients().subscribe(pats => {
      this.patients = pats
    })
  }

  searchPatient() {
    console.log(this.searchKey)
  }

  newPatient() {
    console.log('Creating new patient')
    this.newPatientFormVisible = true;
  }
}
