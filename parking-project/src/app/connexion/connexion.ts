import { Component,inject } from '@angular/core';
import { FormBuilder,FormGroup,Validators,ReactiveFormsModule,AbstractControl,ValidationErrors } from '@angular/forms';
import { UserService } from '../services/user.service';
import { Router, RouterLink } from '@angular/router';
@Component({
  selector: 'app-connexion',
  standalone: true,
  imports: [ReactiveFormsModule,RouterLink],
  templateUrl: './connexion.html',
  styleUrl: './connexion.css',
})
export class Connexion {
 hidePassword = true;
 loginForm:FormGroup;
 userService = inject(UserService);
 private router=inject(Router);
 constructor(private fb:FormBuilder){
  this.loginForm=this.fb.group({
    password: ['',[Validators.required, Validators.minLength(8)]],
    email: ['',[Validators.required, Validators.email]],});
 }
get email() { return this.loginForm.get('email'); }
  get password() { return this.loginForm.get('password'); }
 
 
 async onSubmit() {
  if (this.loginForm.invalid) { 
    this.loginForm.markAllAsTouched();
    return; 
  }

  const email=this.loginForm.value.email;
  const password=this.loginForm.value.password;

  console.log('Données envoyées ', {
    email:email,
    password:password
  }); 
   const user=await this.userService.login(email,password);
 
 if(user){
  console.log("connexion réussie:", user);

  if (user.role==='admin'){
    this.router.navigate(['/administration']);
  }
  else{
  this.router.navigate(['/home']);
  }
 }

 else{
  alert("email ou mot de passe incorrect");
 }
 this.loginForm.reset()
  }
  
}

