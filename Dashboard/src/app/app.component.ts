import { Component } from '@angular/core';
import { AbstractControl, FormControl, FormGroup, Validators } from '@angular/forms';
import { DashboardService } from './services/dashboard.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  
  public isFind: boolean;
  public count: number;
  public maxCount: number;
  public networkMaskFormControl: FormControl;
  public ipStartFormControl: FormControl;
  public ipEndFormControl: FormControl;
  public portFormControl: FormControl;
  public findFormGroup: FormGroup;
  public foundDeviceArr: Array<any>;
  public registeredDeviceArr: Array<any>;

  constructor(
    private dashboardService: DashboardService
  ) {
    this.isFind = false;
    this.count = 0;
    this.maxCount = 1;
    this.networkMaskFormControl = new FormControl('255.255.255.0', [
      Validators.required,
      Validators.pattern(/\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/),
      (abstractControl: AbstractControl) => {
        let bitArr = this.ipToBitArr(abstractControl.value);
        let bit = 1;
        if(!bitArr.every((e) => {
          if(e > bit) {
            return false;
          } else {
            bit = e;
            return true;
          }})) {
          return {
            networkMask: true
          };
        } else {
          return null;
        }
      }
    ]);
    this.ipStartFormControl = new FormControl('192.168.1.', [
      Validators.required,
      Validators.pattern(/\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/)
    ]);
    this.ipEndFormControl = new FormControl('192.168.1.', [
      Validators.required,
      Validators.pattern(/\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/),
      (abstractControl: AbstractControl) => {
        let networkMaskBitArr = this.ipToBitArr(this.networkMaskFormControl.value);
        let ipStartBitArr = this.ipToBitArr(this.ipStartFormControl.value);
        let ipEndBitArr = this.ipToBitArr(abstractControl.value);
        if(!networkMaskBitArr.reduce((previousValue, currentValue, index) => {
          return previousValue && (currentValue == 1 ? ipStartBitArr[index] == ipEndBitArr[index] : true);
        }, true)) {
          return {
            differentNetworks: true
          };
        } else {
          return null;
        }
      }
    ]),
    this.portFormControl = new FormControl('80', [
      Validators.required
    ])
    this.findFormGroup = new FormGroup({
      networkMask: this.networkMaskFormControl,
      ipStart: this.ipStartFormControl,
      ipEnd: this.ipEndFormControl,
      port: this.portFormControl
    });
    this.findFormGroup.markAllAsTouched();
    this.foundDeviceArr = [{
      ip: '127.0.0.1',
      port: 80
    }];
    this.registeredDeviceArr = [];
  }

  private ipToBitArr(networkMask: string): Array<number> {
    return networkMask.split('.')
      .map((e) => {
        return `00000000${parseInt(e).toString(2)}`.slice(-8);
      })
      .reduce((previousValue, currentValue) => {
        return previousValue.concat(currentValue);
      }, '')
      .split('')
      .map((e) => {
        return parseInt(e);
      });
  }

  public findFormGroupNgModelChange(): void {
    Object.keys(this.findFormGroup.controls).forEach((e) => {
      this.findFormGroup.controls[e].updateValueAndValidity();
    });
  }

  public find(): void {
    if(this.findFormGroup.valid) {
      this.isFind = true;
      this.foundDeviceArr = [];
      let addressArr = [];
      let idLength = this.ipToBitArr(this.networkMaskFormControl.value)
        .filter((e) => {
          return e == 0;
        }).length;
      let networkBitStr = this.ipToBitArr(this.ipStartFormControl.value)
        .slice(0, -idLength)
        .join('');
      let idStart = parseInt(this.ipToBitArr(this.ipStartFormControl.value)
        .slice(-idLength)
        .join(''), 2);
      let idEnd = parseInt(this.ipToBitArr(this.ipEndFormControl.value)
        .slice(-idLength)
        .join(''), 2);
      for(let i = idStart; i <= idEnd; i++) {
        if(i != 0 && i != parseInt(Array(idLength).fill('1').join(''), 2)) {
          let ipBitStr = `${networkBitStr}${i.toString(2)}`;
          addressArr.push(`${parseInt(ipBitStr.slice(0, 8), 2)}.${parseInt(ipBitStr.slice(8, 16), 2)}.${parseInt(ipBitStr.slice(16, 24), 2)}.${parseInt(ipBitStr.slice(24, 32), 2)}:${this.portFormControl.value}`);
        }
      }
      if(addressArr.length > 0) {
        this.count = 0;
        this.maxCount = addressArr.length;
        addressArr.forEach((address) => {
          this.dashboardService.find(address)
            .subscribe({
              next: (response) => {
                this.count++;
                console.log(response);
                if(response.success) {
                  this.foundDeviceArr.push({
                    ip: response.ip,
                    port: response.port
                  });
                }
                if(this.count == this.maxCount) {
                  this.isFind = false;
                }
              },
              error: (error) => {
                this.count++;
                console.log(error);
                if(this.count == this.maxCount) {
                  this.isFind = false;
                }
              }
            });
        });
      } else {
        this.isFind = false;
      } 
    }
  }

  public addDevice(device: any): void {
    this.foundDeviceArr.splice(this.foundDeviceArr.indexOf(device), 1);
    this.registeredDeviceArr.push(device);
  }

  public onDeviceRemove(device: any): void {
    this.registeredDeviceArr.splice(this.registeredDeviceArr.indexOf(device), 1);
  }
}
