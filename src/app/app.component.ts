import { Component } from '@angular/core';
import { ElectronService, DatabaseService } from './core/services';
import { TranslateService } from '@ngx-translate/core';
import { APP_CONFIG } from '../environments/environment';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  constructor(
    private electronService: ElectronService,
    private translate: TranslateService,
    private dbService: DatabaseService
  ) {
    this.translate.setDefaultLang('en');

    if (electronService.isElectron) {
      this.dbService.addPatient();
    }
  }
}
