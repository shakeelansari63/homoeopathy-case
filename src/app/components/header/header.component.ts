import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {
  
  // Input for Company Name
  @Input() company: string;
  @Output() drawerToggle: EventEmitter<null> = new EventEmitter();

  constructor() { }

  ngOnInit(): void {
  }

  toggleDrawer() {
    this.drawerToggle.emit();
  }
}
