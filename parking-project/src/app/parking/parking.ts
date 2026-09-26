import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ParkingService, ParkingModel } from '../services/parking.service';
import { RouterLink } from '@angular/router';
@Component({
  selector: 'app-parking',
  standalone:true,
  imports: [CommonModule,RouterLink],
  templateUrl: './parking.html',
  styleUrl: './parking.css',
})
export class Parking implements OnInit {
 parkingService=inject(ParkingService);
 parkings:ParkingModel[]=[];
 chargement=true;
 erreur='';
 
 ngOnInit() {
  this.chargerParkings();
   
 }
 async chargerParkings(){
  try {
  this.parkings=await this.parkingService.getParkings();
  console.log('Parkings sont ammenés:',this.parkings);
  this.chargement=true;
 }
  catch (error){
    console.error('Erreur:',error);
    this.erreur='Impossible de charger les parkings';
    this.chargement=false;
  }

}
}
