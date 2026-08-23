import { Component, OnInit } from '@angular/core';
import {  FormGroup, ReactiveFormsModule,FormBuilder,Validators } from '@angular/forms';
@Component({
  selector: 'app-contact',
  standalone:true,
  imports: [ReactiveFormsModule],
  templateUrl: './contact.html',
  styleUrl: './contact.css',
})
export class Contact implements OnInit{
 contactForm: FormGroup;
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
onSubmit(){} }
