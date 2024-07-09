import {Component, OnInit} from '@angular/core';
import {BehaviorSubject, catchError, combineLatest, map, Observable, of, Subject} from "rxjs";
import {ShipDto} from "../../dtos/ship.dto";
import {ApiService} from "../../services/api.service";
import {AsyncPipe, NgForOf, NgIf, NgOptimizedImage} from "@angular/common";
import {LogoComponent} from "../logo/logo.component";
import {FormsModule} from "@angular/forms";

@Component({
  selector: 'app-ships',
  standalone: true,
  imports: [
    AsyncPipe,
    NgForOf,
    NgIf,
    NgOptimizedImage,
    LogoComponent,
    FormsModule
  ],
  templateUrl: './ships.component.html',
  styleUrl: './ships.component.css'
})
export class ShipsComponent implements OnInit {

  filterText: string = ''
  ships$: Observable<ShipDto[]> = of<ShipDto[]>([])
  filteredShips$: Observable<ShipDto[]> = of<ShipDto[]>([])
  filterSubject$: Subject<string> = new BehaviorSubject<string>('')

  constructor(private api: ApiService) {

  }

  ngOnInit(): void {
    this.ships$ = this.api.getShipsList()
    this.filteredShips$ = combineLatest([
      this.ships$,
      this.filterSubject$,
    ]).pipe(
      map(([ships, filter]) => ships.filter(s => s.name.toLowerCase().includes(filter) || s.description.toLowerCase().includes(filter))),
    )
  }

  onFilterChange() {
    this.filterSubject$.next(this.filterText)
  }
}
