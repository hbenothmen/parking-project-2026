import { HttpClient } from "@angular/common/http";
import { Injectable,inject } from "@angular/core";
import { firstValueFrom } from "rxjs";
export interface ParkingModel{
  id: number;
  nom: string;
  adresse: string;
  nombre_places: number;
  places_disponibles: number;
  prix_heure: number;
  statut: string;
  date_creation: string;   
}
@Injectable({
    providedIn:'root'
})
export class ParkingService{
   private http=inject(HttpClient);
   private apiUrl="https://parking-backend-3ao9.onrender.com/api/parkings";
    async getParkings(): Promise<ParkingModel[]> {
    return firstValueFrom(
      this.http.get<ParkingModel[]>(this.apiUrl)
    );
  }
   async addParking(parking: {
    nom: string;
    adresse: string;
    nombre_places: number;
    prix_heure: number;
  }): Promise<ParkingModel> {

    return firstValueFrom(
      this.http.post<ParkingModel>(this.apiUrl, parking)
    );
  }
  async modifierParking(id: number, parking:{
  nom: string;
  adresse: string;
  nombre_places: number;
  prix_heure: number;
}): Promise<ParkingModel> {
    return firstValueFrom(
      this.http.put<ParkingModel>(
        `${this.apiUrl}/${id}`,
        parking
      )
    );
  }
   async supprimerParking(id: number):Promise<any> {
    return firstValueFrom(
     this.http.delete(
      `${this.apiUrl}/${id}`
    ));
  }
}