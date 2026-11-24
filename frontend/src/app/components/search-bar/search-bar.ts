import { Component, output } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-search-bar',
  imports: [FormsModule],
  templateUrl: './search-bar.html',
  styleUrl: './search-bar.css',
})
export class BarraBusqueda {
  readonly buscar = output<string>();
  consulta = '';

  enviar(): void {
    this.buscar.emit(this.consulta.trim());
  }
}
