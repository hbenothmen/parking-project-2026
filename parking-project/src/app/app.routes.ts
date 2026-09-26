import { Routes } from '@angular/router';
import { Home } from './home/home';
import { Connexion } from './connexion/connexion';
import { Register } from './register/register';
import { Contact } from './contact/contact';
import { Administration } from './administration/administration';
import { Message } from './message/message';
import { Parking } from './parking/parking';
import { GestionParking } from './gestion-parking/gestion-parking';
import { AddParking } from './add-parking/add-parking';
export const routes: Routes = [

{
 path:'home', component:Home},
 {path:'connexion', component:Connexion},
 {path:'register',component:Register},
 {path:'contact',component:Contact},
{path:'administration',component:Administration},
{path:'message',component:Message},
{path:'parking',component:Parking},
{path:'gestionparking',component:GestionParking},
{path:'addparking',component:AddParking}
];
