import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PatientsComponent } from '../components/patients/patients.component'
import { CasesComponent } from '../components/cases/cases.component'
import { HomeComponent } from '../components/home/home.component'
import { SettingComponent } from '../components/setting/setting.component'

const routes: Routes = [
  {path: '', component: HomeComponent},
  {path: 'patients', component: PatientsComponent},
  {path: 'cases', component: CasesComponent},
  {path: 'setting', component: SettingComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
