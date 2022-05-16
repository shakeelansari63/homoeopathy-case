import { Injectable } from '@angular/core';
import { ElectronService } from '../electron/electron.service';

@Injectable({
  providedIn: 'root'
})
export class ConfigService {
  config: any;

  constructor(
    private _electron: ElectronService,
  ) {
    const configFile = this._electron.path.join(__dirname, 'assets/config/app-config.json');
    // read Config File
    const configData = this._electron.fs.readFileSync(configFile, {encoding: 'utf-8', flag: 'r'});

    this.config = JSON.parse(configData);
  }
}
