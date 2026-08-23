import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { FormBuilder,FormGroup,Validators,ReactiveFormsModule,AbstractControl,ValidationErrors } from '@angular/forms';

@Component({
  selector: 'app-connexion',
  standalone: true,
  imports: [ReactiveFormsModule,RouterOutlet],
  templateUrl: './connexion.html',
  styleUrl: './connexion.css',
})
export class Connexion {
 hidePassword = true;
 loginForm:FormGroup;
 constructor(private fb:FormBuilder){
  this.loginForm=this.fb.group({
    password: ['',[Validators.required, Validators.minLength(8)]],
    email: ['',[Validators.required, Validators.email]],});
 }
get email() { return this.loginForm.get('email'); }
  get password() { return this.loginForm.get('password'); }
 
 
 onSubmit() {
  if (this.loginForm.valid) {
    console.log('Données envoyées ', this.loginForm.value);
  }
 }
}

