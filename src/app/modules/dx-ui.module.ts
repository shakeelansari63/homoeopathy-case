import { NgModule } from '@angular/core';
import { DxToolbarModule } from 'devextreme-angular/ui/toolbar';
import { DxButtonModule } from 'devextreme-angular/ui/button';
import { DxDrawerModule } from 'devextreme-angular/ui/drawer';
import { DxListModule } from 'devextreme-angular/ui/list';
import { DxTextBoxModule } from 'devextreme-angular/ui/text-box';
import { DxFormModule } from 'devextreme-angular/ui/form';
import { DxPopupModule } from 'devextreme-angular/ui/popup';
import { DxScrollViewModule } from 'devextreme-angular/ui/scroll-view';
import { DxTextAreaModule } from 'devextreme-angular/ui/text-area';

const uiElements = [
  DxToolbarModule,
  DxButtonModule,
  DxDrawerModule,
  DxListModule,
  DxTextBoxModule,
  DxFormModule,
  DxPopupModule,
  DxScrollViewModule,
  DxTextAreaModule
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
