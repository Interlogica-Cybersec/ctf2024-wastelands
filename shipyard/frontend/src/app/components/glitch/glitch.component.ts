import {Component} from '@angular/core';
import {LogoComponent} from "../logo/logo.component";

@Component({
  selector: 'app-glitch',
  standalone: true,
  imports: [
    LogoComponent,
  ],
  templateUrl: './glitch.component.html',
  styleUrl: './glitch.component.css'
})
export class GlitchComponent {
}
