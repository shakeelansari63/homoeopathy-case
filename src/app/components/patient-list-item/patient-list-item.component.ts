import { Component, OnInit, Input } from '@angular/core';
import { Patient } from '../../models/patient'

@Component({
  selector: 'app-patient-list-item',
  templateUrl: './patient-list-item.component.html',
  styleUrls: ['./patient-list-item.component.scss']
})
export class PatientListItemComponent implements OnInit {

  @Input() patient: Patient;

  constructor() { }

  ngOnInit(): void {
  }

}
