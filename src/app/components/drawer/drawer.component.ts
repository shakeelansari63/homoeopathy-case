import { Component, OnInit, Input } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-drawer',
  templateUrl: './drawer.component.html',
  styleUrls: ['./drawer.component.scss']
})
export class DrawerComponent implements OnInit {

  constructor(private router: Router) { }

  @Input() drawerOpen: boolean;

  navigationItems: any[] = [
    {id: 1, text: 'Home', icon: 'home', path: ''},
    {id: 2, text: 'Patients', icon: 'user', path: 'patients'},
    {id: 3, text: 'Cases', icon: 'doc', path: 'cases'}
  ]

  ngOnInit(): void {
  }

  loadView(evnt: any) {
    console.log(evnt)
    this.router.navigate([evnt.addedItems[0].path])
  }

}
