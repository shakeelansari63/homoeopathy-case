import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PatientsComponent } from '../components/patients/patients.component'
import { CasesComponent } from '../components/cases/cases.component'

const routes: Routes = [
  {path: '', redirectTo: "/", pathMatch: 'full'},
  {path: 'patients', component: PatientsComponent},
  {path: 'cases', component: CasesComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
