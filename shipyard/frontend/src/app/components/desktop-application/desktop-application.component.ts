import {Component} from '@angular/core';
import {HeaderComponent} from "../header/header.component";
import {LogoComponent} from "../logo/logo.component";

@Component({
  selector: 'app-desktop-application',
  standalone: true,
  imports: [
    HeaderComponent,
    LogoComponent
  ],
  templateUrl: './desktop-application.component.html',
  styleUrl: './desktop-application.component.css'
})
export class DesktopApplicationComponent {

  link: string = atob('L2NsaWVudC9zaGlweWFyZC1jbGllbnQtYXBwbGljYXRpb24uamFy');

}
