import { Component } from '@angular/core';
import {LogoComponent} from "../logo/logo.component";
import {FooterComponent} from "../footer/footer.component";
import {HeaderComponent} from "../header/header.component";

@Component({
  selector: 'app-admin-panel',
  standalone: true,
  imports: [
    LogoComponent,
    FooterComponent,
    HeaderComponent
  ],
  templateUrl: './admin-panel.component.html',
  styleUrl: './admin-panel.component.css'
})
export class AdminPanelComponent {

}
