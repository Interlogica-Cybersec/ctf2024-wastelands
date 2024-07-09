import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {ShipDto} from "../dtos/ship.dto";

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(
    private http: HttpClient,
  ) {
  }

  getShipsList(): Observable<ShipDto[]> {
    return this.http.get<ShipDto[]>('/api/ships');
  }
}
