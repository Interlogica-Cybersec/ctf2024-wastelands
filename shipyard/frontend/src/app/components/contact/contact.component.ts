import {Component} from '@angular/core';
import {LogoComponent} from "../logo/logo.component";
import {ActivatedRoute} from "@angular/router";
import {AsyncPipe, NgIf} from "@angular/common";

@Component({
  selector: 'app-contact',
  standalone: true,
  imports: [
    LogoComponent,
    NgIf,
    AsyncPipe
  ],
  templateUrl: './contact.component.html',
  styleUrl: './contact.component.css'
})
export class ContactComponent {

  constructor(protected route: ActivatedRoute) {
  }

}
