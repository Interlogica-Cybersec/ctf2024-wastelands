import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ShipsComponent } from './ships.component';

describe('ShipsComponent', () => {
  let component: ShipsComponent;
  let fixture: ComponentFixture<ShipsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ShipsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ShipsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
