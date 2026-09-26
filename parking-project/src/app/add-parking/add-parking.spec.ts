import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddParking } from './add-parking';

describe('AddParking', () => {
  let component: AddParking;
  let fixture: ComponentFixture<AddParking>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AddParking],
    }).compileComponents();

    fixture = TestBed.createComponent(AddParking);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
