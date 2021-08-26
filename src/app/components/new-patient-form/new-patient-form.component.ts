import { Component, ComponentFactoryResolver, OnInit } from '@angular/core';
import { Patient } from '../../models/patient';
import { PatientsDataService } from '../../services/patients-data.service'

@Component({
  selector: 'app-new-patient-form',
  templateUrl: './new-patient-form.component.html',
  styleUrls: ['./new-patient-form.component.scss']
})
export class NewPatientFormComponent implements OnInit {

  constructor(private pat: PatientsDataService) { }

  genders: Array<{gender: string, code: string}>;
  maritalStatus: Array<{status: string, code: string}>;
  genderOptions: any;
  msOptions: any;
  submitButtonOptions: any;
  phoneOptions: any;


  patientData: Patient;

  ngOnInit(): void {
    this.genders = [
      {gender: 'Male', code: 'M'},
      {gender: 'Female', code: 'F'},
      {gender: 'Other', code: 'O'}
    ]

    this.genderOptions = {
      items: this.genders, 
      valueExpr: 'code', 
      displayExpr: 'gender',
      searchEnabled: true
    }

    this.maritalStatus = [
      {status: 'Married', code: 'M'},
      {status: 'Single', code: 'S'},
      {status: 'Committed', code: 'C'},
      {status: 'No Answer', code: 'N'},
    ]

    this.msOptions = {
      items: this.maritalStatus, 
      valueExpr: 'code', 
      displayExpr: 'status',
      searchEnabled: true
    }

    this.phoneOptions = {
      mask: '000 000 0000'
    }

    this.submitButtonOptions = {
      text: 'Save Patient', 
      type: 'default', 
      useSubmitBehavior: true
    }

    this.patientData = {
      firstName: '',
      lastName: '',
      age: null,
      gender: '',
      phone: '',
      address: '',
      occupation: '',
      maritalStatus: '',
      reference: '',
      datetm: new Date()
    }
  }

  savePatient() {
    console.log(this.patientData)

    // Saeve Patient
    this.pat.newPatient(this.patientData)
  }

}
