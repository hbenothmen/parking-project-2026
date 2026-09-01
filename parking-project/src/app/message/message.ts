import { Component, OnInit,inject } from '@angular/core';
import { UserService } from '../services/user.service';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
@Component({
  selector: 'app-message',
  standalone:true,
  imports: [CommonModule,RouterLink],
  templateUrl: './message.html',
  styleUrl: './message.css',
})
export class Message implements OnInit {
  userService= inject(UserService);
  messages: any[]=[];
  chargement = true;
  erreur='';
  ngOnInit(){
    this.chargerMessages();
    
  }
  //chargement des messages
  async chargerMessages(): Promise<void> {

  console.log('Chargement des messages...');

  this.chargement = true;
  this.erreur = '';

  try {

    const data = await this.userService.getMessage();

    console.log('Data reçue par Angular :', data);

    this.messages = data;

  } catch (error) {

    console.error(
      'Erreur lors du chargement des messages :',
      error
    );

    this.erreur = 'Impossible de charger les messages';

  } finally {

    this.chargement = false;

  }
}
  // chargerMessages():void {
  //   console.log('Chargement des messages...');
  //   this.chargement = true;
  //   this.erreur = '';

  //   this.userService.getMessage().subscribe({
  //     next: (data) => {
  //       console.log('data recue par angular:',data);
  //       this.messages = data;
  //       this.chargement = false;
  //     },
  //     error:(error) =>{

  //       console.error('Erreur lors du chargement des messages',error);
  //       this.erreur='Impossible de charger les messages';
  //       this.chargement= false;
  //     }
  //   });
  // }
supprimerMessage(id:number):void{
 const confirmation=confirm(
  'Voulez vous vraiment supprimer ce message?');
  if (!confirmation){
    return;
  }
  this.userService.supprimerMessage(id).subscribe({
    next:()=> {
      this.messages = this.messages.filter(
        message=>message.id!=id
      );
      alert('Message supprimé avec succès');
    },
    error: (error)=>{
      console.error('Erreur lors de la suppression:',error);
    alert('Erreur lors de la suppression du message');
    }
  });
}
}
