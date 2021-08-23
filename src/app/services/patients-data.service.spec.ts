import { TestBed } from '@angular/core/testing';

import { PatientsDataService } from './patients-data.service';

describe('PatientsDataService', () => {
  let service: PatientsDataService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PatientsDataService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
