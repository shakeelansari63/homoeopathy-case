import { NgModule } from '@angular/core';
import { DxToolbarModule } from 'devextreme-angular/ui/toolbar';
import { DxButtonModule } from 'devextreme-angular/ui/button';
import { DxDrawerModule } from 'devextreme-angular/ui/drawer';
import { DxListModule } from 'devextreme-angular/ui/list';

const uiElements = [
  DxToolbarModule,
  DxButtonModule,
  DxDrawerModule,
  DxListModule
]

@NgModule({
  declarations: [],
  imports: [
    uiElements
  ],
  exports: [
    uiElements
  ]
})
export class DxUiModule { }
