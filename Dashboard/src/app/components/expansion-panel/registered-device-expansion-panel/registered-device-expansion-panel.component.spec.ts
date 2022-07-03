import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RegisteredDeviceExpansionPanelComponent } from './registered-device-expansion-panel.component';

describe('RegisteredDeviceExpansionPanelComponent', () => {
  let component: RegisteredDeviceExpansionPanelComponent;
  let fixture: ComponentFixture<RegisteredDeviceExpansionPanelComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RegisteredDeviceExpansionPanelComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RegisteredDeviceExpansionPanelComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
