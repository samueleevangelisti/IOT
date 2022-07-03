import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class DashboardService {

  constructor(
    private httpClient: HttpClient
  ) { }

  public find(address: string): Observable<any> {
    return this.httpClient.get(`http://${address}/iotfind`);
  }

  public getDashboard(address: string): Observable<any> {
    return this.httpClient.get(`http://${address}/dashboard`);
  }

  public setDashboard(address: string, configObj: any): Observable<any> {
    return this.httpClient.post(`http://${address}/dashboard`, configObj);
  }
  
}
