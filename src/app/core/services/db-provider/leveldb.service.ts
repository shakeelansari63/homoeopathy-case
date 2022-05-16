import { Injectable } from '@angular/core';
import { IDB } from './idb.interface';
import { Guid } from 'guid-typescript';
import { Level } from 'level';

// Get Sqlite Service
import * as level from 'level'
import { ElectronService } from '../electron/electron.service';
import { ConfigService } from '../config/config.service';

@Injectable({
  providedIn: 'root'
})
export class LevelDbService implements IDB {
  //leveldb: typeof level;

  dbProtocol: string;
  dbPath: string;

  dbUrl: string;

  constructor(
    private _electron: ElectronService,
    private _config: ConfigService,
  ) {
    //{ this.leveldb } = window.require('level');

    this.dbPath = this._config.config.dbOptions.path;
    this.dbProtocol = this._config.config.dbOptions.protocol;

    // Set Path for File
    if (this.dbProtocol === 'file') {
      this.dbUrl = this._electron.path.join(__dirname, this.dbPath);

      // Create directory if not exist
      if (!this._electron.fs.existsSync(this.dbUrl))
        this._electron.fs.mkdirSync(this.dbUrl);
    }

    else {
      this.dbUrl = this.dbPath;
    }
  }

  checkDbAccess(dbName: string) : boolean {
    return this._electron.fs.existsSync(this.getFullDbPath(dbName));
  }

  getFullDbPath(dbName: string) : string {
    return this._electron.path.join(this.dbUrl, dbName);
  }

  async addData(dbName: string, detail: any) {
    const dbFile = this.getFullDbPath(dbName);

    const db = new Level<string, any>(dbFile, { createIfMissing: true });

    const key = Guid.create().toString();

    await db.put(key, detail, err => console.log(err));
  }

  handleError(err) {
    console.log(err);
    throw err;
  }
}
