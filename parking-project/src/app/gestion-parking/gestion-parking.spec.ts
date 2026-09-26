import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GestionParking } from './gestion-parking';

describe('GestionParking', () => {
  let component: GestionParking;
  let fixture: ComponentFixture<GestionParking>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GestionParking],
    }).compileComponents();

    fixture = TestBed.createComponent(GestionParking);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
