import { Component,inject, OnInit } from '@angular/core';
import { ParkingService,ParkingModel } from '../services/parking.service';
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
@Component({
  selector: 'app-gestion-parking',
  standalone:true,
  imports: [RouterLink,CommonModule],
  templateUrl: './gestion-parking.html',
  styleUrl: './gestion-parking.css',
})
export class GestionParking implements OnInit{
  parkingService=inject(ParkingService)
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
