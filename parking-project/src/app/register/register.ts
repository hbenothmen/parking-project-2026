import { Component, OnInit,inject } from '@angular/core';
import {FormBuilder, FormGroup,Validators,AbstractControl,ValidationErrors,ReactiveFormsModule} from '@angular/forms';
import { UserService } from '../services/user.service';
import { RouterLink } from '@angular/router';
import { User } from '../models/user.model';
@Component({
  selector: 'app-register',
  standalone:true,
  imports: [ReactiveFormsModule,RouterLink],
  templateUrl: './register.html',
  styleUrl: './register.css',
})
export class Register implements OnInit{

  hidePassword = true;
  registerForm: FormGroup;
  passwordRule = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
  userService=inject(UserService);
  constructor(private fb: FormBuilder) {

    this.registerForm = this.fb.group({

      nom: ['', Validators.required],

      email: ['', [
        Validators.required,
        Validators.email
      ]],

      password: ['', [
        Validators.required,
        Validators.pattern(this.passwordRule)
      ]],

      confirmPassword: ['', Validators.required]

    },
    {
      validators: this.passwordMatchValidator
    });

  }

  passwordMatchValidator(control: AbstractControl): ValidationErrors | null {

    const password = control.get('password')?.value;
    const confirm = control.get('confirmPassword')?.value;

    return password === confirm
      ? null
      : { passwordMismatch: true };
  }

  ngOnInit(){
    this.userService.loadUsers();
  }
  async onSubmit() {
//En Angular, cela force l'affichage immédiat des messages d'erreur
// de validation sous chaque champ non valid
    if(this.registerForm.invalid){
      this.registerForm.markAllAsTouched();
      return;
    }
    //Récupère les valeurs actuelles saisie
    // dans les champs du formulaire
    // et les assigne au propriétés de l'objet.
    const user: User={
     nom: this.registerForm.value.nom,
     email: this.registerForm.value.email,
     password: this.registerForm.value.password 
    };
    console.log("utilisateur à ajouté:",user);
    //Envoie une requête HTTP (généralement POST)
    // au serveur backend via UserService) pour 
    // enregistrer l'utilisateur en base de données.
    await this.userService.addUser(user);
    this.registerForm.reset();
    console.log("utilisateur ajouté avec succés")
  
  }

    }
   

  
