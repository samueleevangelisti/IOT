import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { DashboardService } from 'src/app/services/dashboard.service';

@Component({
  selector: 'app-registered-device-expansion-panel',
  templateUrl: './registered-device-expansion-panel.component.html',
  styleUrls: ['./registered-device-expansion-panel.component.css']
})
export class RegisteredDeviceExpansionPanelComponent implements OnInit {

  @Input()
  public device: any;
  @Output()
  private onRemove = new EventEmitter();

  public isLoading: boolean;
  public formGroup: FormGroup;
  
  constructor(
    private matSnackbar: MatSnackBar,
    private dashboardService: DashboardService
  ) {
    this.isLoading = false;
    this.formGroup = new FormGroup({
      PIN_DHT11: new FormControl(''),
      PIN_MQ2_AO: new FormControl(''),
      PIN_MQ2_DO: new FormControl(''),
      ESP32_ID: new FormControl('', [
        Validators.required,
        Validators.maxLength(20)
      ]),
      ESP32_LATITUDE: new FormControl('', [
        Validators.required
      ]),
      ESP32_LONGITUDE: new FormControl('', [
        Validators.required
      ]),
      SAMPLE_FREQUENCY: new FormControl('', [
        Validators.required
      ]),
      MIN_GAS_VALUE: new FormControl('', [
        Validators.required,
        Validators.min(200),
        Validators.max(10000)
      ]),
      MAX_GAS_VALUE: new FormControl('', [
        Validators.required,
        Validators.min(200),
        Validators.max(10000)
      ]),
      COMMUNICATION_PROTOCOL: new FormControl('', [
        Validators.required,
        Validators.min(0),
        Validators.max(2)
      ]),
      MQTT_SERVER: new FormControl('', [
        Validators.maxLength(15)
      ]),
      MQTT_USER: new FormControl('', [
        Validators.maxLength(20)
      ]),
      MQTT_PASSWORD: new FormControl('', [
        Validators.maxLength(20)
      ]),
      MQTT_TOPIC: new FormControl('', [
        Validators.maxLength(20)
      ]),
      COAP_SERVER: new FormControl('', [
        Validators.maxLength(15)
      ]),
      COAP_URL: new FormControl('', [
        Validators.maxLength(20)
      ]),
      HTTP_SEND_URL: new FormControl('', [
        Validators.maxLength(50)
      ]),
    });
  }

  ngOnInit(): void {
    this.refresh();
  }

  public remove(): void {
    this.onRemove.emit(this.device);
  }

  public refresh(): void {
    this.isLoading = true;
    this.dashboardService.getDashboard(`${this.device.ip}:${this.device.port}`)
      .subscribe({
        next: (response) => {
          console.log(response);
          if(response.success) {
            this.formGroup.controls['PIN_DHT11'].setValue(response.data.PIN_DHT11);
            this.formGroup.controls['PIN_MQ2_AO'].setValue(response.data.PIN_MQ2_AO);
            this.formGroup.controls['PIN_MQ2_DO'].setValue(response.data.PIN_MQ2_DO);
            this.formGroup.controls['ESP32_ID'].setValue(response.data.ESP32_ID);
            this.formGroup.controls['ESP32_LATITUDE'].setValue(response.data.ESP32_LATITUDE);
            this.formGroup.controls['ESP32_LONGITUDE'].setValue(response.data.ESP32_LONGITUDE);
            this.formGroup.controls['SAMPLE_FREQUENCY'].setValue(response.data.SAMPLE_FREQUENCY);
            this.formGroup.controls['MIN_GAS_VALUE'].setValue(response.data.MIN_GAS_VALUE);
            this.formGroup.controls['MAX_GAS_VALUE'].setValue(response.data.MAX_GAS_VALUE);
            this.formGroup.controls['COMMUNICATION_PROTOCOL'].setValue(response.data.COMMUNICATION_PROTOCOL);
            this.formGroup.controls['MQTT_SERVER'].setValue(response.data.MQTT_SERVER);
            this.formGroup.controls['MQTT_USER'].setValue(response.data.MQTT_USER);
            this.formGroup.controls['MQTT_PASSWORD'].setValue(response.data.MQTT_PASSWORD);
            this.formGroup.controls['MQTT_TOPIC'].setValue(response.data.MQTT_TOPIC);
            this.formGroup.controls['COAP_SERVER'].setValue(response.data.COAP_SERVER);
            this.formGroup.controls['COAP_URL'].setValue(response.data.COAP_URL);
            this.formGroup.controls['HTTP_SEND_URL'].setValue(response.data.HTTP_SEND_URL);
          }
          this.isLoading = false;
          this.matSnackbar.open(`Got dashboard for ${this.device.ip}:${this.device.port}`, 'Close');
        },
        error: (error) => {
          console.log(error);
          this.isLoading = false;
          this.matSnackbar.open(`Unable get dashboard for ${this.device.ip}:${this.device.port}`, 'Close');
        }
      });
  }

  public setValues(): void {
    if(this.formGroup.valid) {
      this.isLoading = true;
      this.dashboardService.setDashboard(`${this.device.ip}:${this.device.port}`, this.formGroup.value)
        .subscribe({
          next: (response) => {
            console.log(response);
            this.matSnackbar.open(`Set dashboard for ${this.device.ip}:${this.device.port}`, 'Close');
            this.refresh();
          },
          error: (error) => {
            console.log(error);
            this.isLoading = false;
            this.matSnackbar.open(`Unable set dashboard for ${this.device.ip}:${this.device.port}`, 'Close');
          }
        });
    }
  }

}
