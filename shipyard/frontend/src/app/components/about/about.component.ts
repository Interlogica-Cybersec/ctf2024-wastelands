import { Component } from '@angular/core';
import {LogoComponent} from "../logo/logo.component";

@Component({
  selector: 'app-about',
  standalone: true,
    imports: [
        LogoComponent
    ],
  templateUrl: './about.component.html',
  styleUrl: './about.component.css'
})
export class AboutComponent {

}
