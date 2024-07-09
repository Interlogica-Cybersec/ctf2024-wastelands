import {Routes} from '@angular/router';
import {HomeComponent} from "./components/home/home.component";
import {ShipsComponent} from "./components/ships/ships.component";
import {GlitchComponent} from "./components/glitch/glitch.component";
import {AdminPanelComponent} from "./components/admin-panel/admin-panel.component";
import {DesktopApplicationComponent} from "./components/desktop-application/desktop-application.component";
import {AboutComponent} from "./components/about/about.component";
import {ContactComponent} from "./components/contact/contact.component";

export const routes: Routes = [
  {path: '', component: HomeComponent},
  {path: 'ships', component: ShipsComponent},
  {path: 'glitch', component: GlitchComponent},
  {path: 'admin', component: AdminPanelComponent},
  {path: 'desktop-application', component: DesktopApplicationComponent},
  {path: 'about', component: AboutComponent},
  {path: 'contact', component: ContactComponent},
];
