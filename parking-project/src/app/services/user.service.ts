import { HttpClient } from "@angular/common/http";
import { Injectable, inject,signal } from "@angular/core";
import { firstValueFrom } from "rxjs";
import { User } from "../models/user.model";
@Injectable({
    providedIn:'root'
})
export class UserService{
    private http=inject(HttpClient);
     apiUrl="http://127.0.0.1:5000/api/users";
     loginUrl="http://127.0.0.1:5000/api/login";
     messageUrl="http://localhost:5000/api/messages"
    // flask api enpoint
//Manage tasks state using Angular Signals for fast updates without Zone.js
users=signal<User[]>([]);
//utilisateur actuellement connecté (on va stocker l'utilisateur
// dans un signal pour masquer l'icone de reservation
// tant que l 'utilisateur n'est pas connecté)
currentUser =signal<User|null>(null);
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
        return newUser;
    }
     catch(error){
    console.error("erreur d'ajouter user:",error);
    return null;
}
}
async login(email: string, password: string){
   try{
    const user = await firstValueFrom(
        this.http.post<User>(
            this.loginUrl,
            {
                email: email,
                password: password
            }
        )

    );
    //Enregistrer l'utilisateur connecté
    this.currentUser.set(user);

    return user;

   } catch(error){

    console.error("erreur de connexion:",error);
    return null;
   }
}
//partie administration
//envoyer message
envoyerMessage(message: any) {
    return this.http.post(this.messageUrl, message);
}
//récuperer les messages
//getMessage(){
   // return this.http.get<any[]>(this.messageUrl);
//}
async getMessage(): Promise<any[]> {

  return firstValueFrom(
    this.http.get<any[]>(this.messageUrl)
  );

}
//supprimer un message
supprimerMessage(id:number){
    return this.http.delete(`${this.messageUrl}/${id}`);
}
//déconnexion
logout(){
    this.currentUser.set(null);
}
}