import {Component, OnInit} from '@angular/core';
import {ApiService} from "../../services/api.service";
import {Observable, of} from "rxjs";
import {ShipDto} from "../../dtos/ship.dto";
import {AsyncPipe, NgForOf, NgIf, NgOptimizedImage} from "@angular/common";
import {LogoComponent} from "../logo/logo.component";
import {FooterComponent} from "../footer/footer.component";
import {HeaderComponent} from "../header/header.component";

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    AsyncPipe,
    NgForOf,
    NgIf,
    LogoComponent,
    FooterComponent,
    HeaderComponent,
    NgOptimizedImage
  ],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent implements OnInit {

  ships$: Observable<ShipDto[]> = of<ShipDto[]>([])

  constructor(private api: ApiService) {

  }

  ngOnInit(): void {
    this.ships$ = this.api.getShipsList()
  }

}
