import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http'

import { DxUiModule } from './modules/dx-ui.module';
import { AppRoutingModule } from './modules/app-routing.module';

import { AppComponent } from './app.component';
import { HeaderComponent } from './components/header/header.component';
import { FooterComponent } from './components/footer/footer.component';
import { DrawerComponent } from './components/drawer/drawer.component';
import { PatientsComponent } from './components/patients/patients.component';
import { CasesComponent } from './components/cases/cases.component';
import { HomeComponent } from './components/home/home.component';
import { SettingComponent } from './components/setting/setting.component';
import { NewPatientFormComponent } from './components/new-patient-form/new-patient-form.component';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    FooterComponent,
    DrawerComponent,
    PatientsComponent,
    CasesComponent,
    HomeComponent,
    SettingComponent,
    NewPatientFormComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FontAwesomeModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    DxUiModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
