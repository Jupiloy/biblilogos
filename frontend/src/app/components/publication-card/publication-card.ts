import { Component, input, output } from '@angular/core';
import { Publicacion } from '../../core/models/library.models';

@Component({
  selector: 'app-publication-card',
  imports: [],
  templateUrl: './publication-card.html',
  styleUrl: './publication-card.css',
})
export class TarjetaPublicacion {
  readonly publicacion = input.required<Publicacion>();
  readonly motivo = input<string>();
  readonly seleccionada = output<Publicacion>();
}
