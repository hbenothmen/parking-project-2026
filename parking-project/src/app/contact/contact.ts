import { Component, OnInit, inject } from '@angular/core';
import {  FormGroup, ReactiveFormsModule,FormBuilder,Validators } from '@angular/forms';
import { UserService } from '../services/user.service';
import { RouterLink } from '@angular/router';
@Component({
  selector: 'app-contact',
  standalone:true,
  imports: [ReactiveFormsModule,RouterLink],
  templateUrl: './contact.html',
  styleUrl: './contact.css',
})
export class Contact implements OnInit{
 contactForm: FormGroup;

 userService=inject(UserService);

constructor(private fb: FormBuilder) {

    this.contactForm = this.fb.group({

      nom: ['', Validators.required],

      email: ['', [
        Validators.required,
        Validators.email
      ]],
      message:['', Validators.required]

},);
}
 ngOnInit(){
    
  }
onSubmit(){
  if (this.contactForm.invalid){
    this.contactForm.markAllAsTouched();
    return;
  }
  const message={
    nom:this.contactForm.value.nom,
    email:this.contactForm.value.email,
    message:this.contactForm.value.message
  };

  this.userService.envoyerMessage(message).subscribe({
    next: (response) => {
      alert('Votre message a été envoyé à l’administrateur');
      this.contactForm.reset();
    },
    error: (error) => {
      console.error('Erreur lors de l’envoi du message :', error);
    alert('Une erreur est survenue lors de l’envoi du message')
    }
  });
} 
}
