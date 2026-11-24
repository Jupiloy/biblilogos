import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import {
  EstadisticasBiblioteca,
  Publicacion,
  Recomendacion,
} from '../models/library.models';

@Injectable({ providedIn: 'root' })
export class ServicioBiblioteca {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = 'http://localhost:8000/api';

  buscar(consulta = '', genero = 'todos'): Observable<Publicacion[]> {
    const params = new HttpParams()
      .set('consulta', consulta)
      .set('genero', genero)
      .set('limit', '20');
    return this.http.get<Publicacion[]>(`${this.apiUrl}/publicaciones`, { params });
  }

  recomendar(isbn: string): Observable<Recomendacion[]> {
    return this.http.get<Recomendacion[]>(`${this.apiUrl}/recomendaciones/${isbn}`);
  }

  obtenerEstadisticas(): Observable<EstadisticasBiblioteca> {
    return this.http.get<EstadisticasBiblioteca>(`${this.apiUrl}/estadisticas`);
  }
}
