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

  public find(): Observable<any> {
    let addressArr = [];
      for(let i = 1; i < 255; i++) {
        addressArr.push(`192.168.1.${i}`);
      }
    return this.httpClient.post(`${environment.baseUrl}/iotfind`, {
      addressArr: addressArr
    });
  }

  public getdashboard(device: any): Observable<any> {
    return this.httpClient.post(`${environment.baseUrl}/getdashboard`, {
      url: `http://${device.ip}:${device.port}/dashboard`
    });
  }

  public subscribe(device: any): Observable<any> {
    return this.httpClient.post(`${environment.baseUrl}/subscribe`, {
      deviceUrl: `http://${device.ip}:${device.port}/subscribe`,
      subscribeUrl: 'http://192.168.1.2:8080/send'
    });
  }
  
}
