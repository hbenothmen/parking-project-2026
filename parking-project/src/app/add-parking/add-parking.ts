import { Component, inject } from '@angular/core';
import { ParkingService } from '../services/parking.service';
import { FormGroup,Validators,FormBuilder,ReactiveFormsModule } from '@angular/forms';
import { UserService } from '../services/user.service';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
@Component({
  selector: 'app-add-parking',
  standalone:true,
  imports: [CommonModule,RouterLink,ReactiveFormsModule],
  templateUrl: './add-parking.html',
  styleUrl: './add-parking.css',
})
export class AddParking {
  parkingService=inject(ParkingService)
  userService=inject(UserService)

  parkingForm:FormGroup;
  
   constructor(private fb: FormBuilder) {

    this.parkingForm = this.fb.group({

      nom: ['', Validators.required],

      adresse: ['', Validators.required,
        
      ],

      nombre_places: ['', Validators.required
      ],

      prix_heure: ['', Validators.required]

    }
    );
  }
  
    async onSubmit() {
  //En Angular, cela force l'affichage immédiat des messages d'erreur
  // de validation sous chaque champ non valid
      if(this.parkingForm.invalid){
        this.parkingForm.markAllAsTouched();
        return;
      }
      //Récupère les valeurs actuelles saisie
      // dans les champs du formulaire
      // et les assigne au propriétés de l'objet.
      const parking={
       nom: this.parkingForm.value.nom,
       adresse: this.parkingForm.value.adresse,
       nombre_places: this.parkingForm.value.nombre_places,
       prix_heure:this.parkingForm.value.prix_heure
      
      };
      console.log("parking à ajouté:",parking);
      //Envoie une requête HTTP (généralement POST)
      // au serveur backend via parkingService) pour 
      // enregistrer le parking en base de données.
      try{
      const resultat=await this.parkingService.addParking(parking);
      
      console.log("utilisateur ajouté avec succés",resultat)
      
      this.parkingForm.reset();

    } catch(error:any){
      console.error("Erreur lors de l'ajout du parking:",error)
    console.error("Erreur complète :", error);
  console.error("Status :", error.status);
  console.error("Message :", error.message);
  console.error("Erreur backend :", error.error);
    }
    }
  }


