import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DesktopApplicationComponent } from './desktop-application.component';

describe('DesktopApplicationComponent', () => {
  let component: DesktopApplicationComponent;
  let fixture: ComponentFixture<DesktopApplicationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DesktopApplicationComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(DesktopApplicationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
