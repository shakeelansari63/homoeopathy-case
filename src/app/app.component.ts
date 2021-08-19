import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  companyName = 'Barqat Homoeopathy'
  
  isDrawerOpen: boolean = false;

  toggleDrawerOpen() {
    this.isDrawerOpen = !this.isDrawerOpen;
  }
}
