import { HttpClient } from "@angular/common/http";
import { Injectable, inject,signal } from "@angular/core";
import { firstValueFrom } from "rxjs";
import { User } from "../models/user.model";
@Injectable({
    providedIn:'root'
})
export class UserService{
    private http=inject(HttpClient);
    private apiUrl="http://127.0.0.1:5000/api/users";// flask api enpoint
//Manage tasks state using Angular Signals for fast updates without Zone.js
users=signal<User[]>([]);
//Récupérer les utilisateurs
async loadUsers(){
    try{
        const data=await firstValueFrom(
         this.http.get<User[]>(this.apiUrl)
            );
        this.users.set(data);
    }
    catch (error){
        console.error("Erreur de téléchargement:", error);
    }
}
//add user
async addUser(user:User){
    try{
        const newUser=await firstValueFrom(
            this.http.post<User>(this.apiUrl, user)
        );
        this.users.update(
          oldUsers=>[...oldUsers, newUser]
        );
    }
     catch(error){
    console.error("erreur d'ajouter user:",error);
}
}

}