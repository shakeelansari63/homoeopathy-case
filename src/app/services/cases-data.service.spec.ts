import { TestBed } from '@angular/core/testing';

import { CasesDataService } from './cases-data.service';

describe('CasesDataService', () => {
  let service: CasesDataService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CasesDataService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
