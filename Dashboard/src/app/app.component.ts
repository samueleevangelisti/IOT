import { ChangeDetectorRef, Component } from '@angular/core';
import { environment } from 'src/environments/environment';
import { DashboardService } from './services/dashboard.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  
  public isLoading: boolean;
  private eventSource: EventSource;
  public count: number;
  public maxCount: number;
  public foundDeviceArr: Array<any>;
  public registeredDeviceArr: Array<any>;

  constructor(
    private changeDetectorRef: ChangeDetectorRef,
    private dashboardService: DashboardService
  ) {
    window.addEventListener('unload', () => {
      this.eventSource.close();
    });
    this.isLoading = true;
    this.eventSource = new EventSource(`${environment.baseUrl}/sse`);
    this.eventSource.addEventListener('message', (message) => {
      let messageObj = JSON.parse(message.data);
      console.log(messageObj);
      switch(messageObj.event) {
        case 'connect':
          this.isLoading = false;
          break;
        case 'iotfind-request':
          if(messageObj.data) {
            this.isLoading = true;
          } else {
            this.isLoading = false;
          }
          break;
        case 'iotfind-data':
          if(messageObj.data.success) {
            this.foundDeviceArr.push(messageObj.data.data);
          }
          this.count = messageObj.data.count;
          this.maxCount = messageObj.data.maxCount;
          break;
      }
      this.changeDetectorRef.markForCheck();
    });
    this.count = 0;
    this.maxCount = 1;
    this.foundDeviceArr = [];
    this.registeredDeviceArr = [];
  }

  public getDeviceDashboard(device: any): string {
    return JSON.stringify(device.dashboard, null, 2);
  }

  public find(): void {
    this.dashboardService.find()
      .subscribe({
        next: (response) => {
          console.log(response);
        },
        error: (error) => {
          console.log(error);
        }});
  }

  public addDevice(device: any): void {
    this.foundDeviceArr.splice(this.foundDeviceArr.indexOf(device), 1);
    this.registeredDeviceArr.push(device);
  }

  public removeDevice(device: any): void {
    this.registeredDeviceArr.splice(this.registeredDeviceArr.indexOf(device), 1);
  }

  public refresh(device: any) {
    this.dashboardService.getdashboard(device)
      .subscribe({
        next: (response) => {
          console.log(response);
          device.dashboard = response;
        },
        error: (error) => {
          console.log(error);
        }
      });
  }

  public subscribe(device: any): void {
    this.dashboardService.subscribe(device)
      .subscribe({
        next: (response) => {
          console.log(response);
        },
        error: (error) => {
          console.log(error);
        }
      });
  }
}
