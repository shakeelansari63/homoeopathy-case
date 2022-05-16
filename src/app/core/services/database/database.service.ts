import { Injectable } from '@angular/core';
import { ConfigService } from '../config/config.service';
import { LevelDbService } from '../db-provider/leveldb.service';

@Injectable({
  providedIn: 'root'
})
export class DatabaseService {
  patientDb: string;
  caseDb: string;
  configDb: string;

  constructor(
    private _dbProvider: LevelDbService,
    private _config: ConfigService
  ) {
    this.patientDb = this._config.config.dbOptions.schemas.patientDb;
    this.caseDb = this._config.config.dbOptions.schemas.caseDb;
    this.configDb = this._config.config.dbOptions.schemas.configDb;
  }

  getAllPatients() {
    this._dbProvider.checkDbAccess(this.patientDb);
  }

  addPatient() {
    this._dbProvider.addData(this.patientDb, {'a': 1});
  }
}
