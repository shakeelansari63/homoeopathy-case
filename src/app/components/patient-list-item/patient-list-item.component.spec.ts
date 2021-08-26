import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PatientListItemComponent } from './patient-list-item.component';

describe('PatientListItemComponent', () => {
  let component: PatientListItemComponent;
  let fixture: ComponentFixture<PatientListItemComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PatientListItemComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PatientListItemComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
