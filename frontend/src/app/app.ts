import { Component, inject, signal } from '@angular/core';
import { TarjetaPublicacion } from './components/publication-card/publication-card';
import { BarraBusqueda } from './components/search-bar/search-bar';
import { Sidebar } from './components/sidebar/sidebar';
import { ServicioBiblioteca } from './core/services/library.service';
import {
  EstadisticasBiblioteca,
  Publicacion,
  Recomendacion,
} from './core/models/library.models';

@Component({
  selector: 'app-root',
  imports: [Sidebar, BarraBusqueda, TarjetaPublicacion],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  private readonly biblioteca = inject(ServicioBiblioteca);

  readonly barraLateralOculta = signal(false);
  readonly seRealizoBusqueda = signal(false);
  readonly estaBuscando = signal(false);
  readonly error = signal('');
  readonly publicaciones = signal<Publicacion[]>([]);
  readonly recomendaciones = signal<Recomendacion[]>([]);
  readonly estadisticas = signal<EstadisticasBiblioteca | null>(null);
  readonly vista = signal<'buscar' | 'explorar' | 'guardados'>('buscar');
  readonly categorias = [
    { nombre: 'Literatura', consulta: 'literature' },
    { nombre: 'Ciencia', consulta: 'science' },
    { nombre: 'Historia', consulta: 'history' },
    { nombre: 'Filosofía', consulta: 'philosophy' },
    { nombre: 'Tecnología', consulta: 'technology' },
    { nombre: 'Arte', consulta: 'art' },
  ];
  readonly publicacionAbierta = signal<Publicacion | null>(null);
  readonly publicacionesGuardadas = signal<Publicacion[]>(
    JSON.parse(localStorage.getItem('bibliologos_guardados') ?? '[]'),
  );

  constructor() {
    this.cargarEstadisticas();
  }

  private cargarEstadisticas(): void {
    this.biblioteca.obtenerEstadisticas().subscribe({
      next: (estadisticas) => this.estadisticas.set(estadisticas),
      error: () => this.error.set('No fue posible cargar las estadísticas.'),
    });
  }

  buscar(consulta: string): void {
    this.vista.set('buscar');
    this.seRealizoBusqueda.set(true);
    this.estaBuscando.set(true);
    this.error.set('');
    this.biblioteca.buscar(consulta).subscribe({
      next: (publicaciones) => {
        this.publicaciones.set(publicaciones);
        this.estaBuscando.set(false);
        this.recomendaciones.set([]);
      },
      error: () => {
        this.estaBuscando.set(false);
        this.error.set('La búsqueda no pudo completarse.');
      },
    });
  }

  seleccionarPublicacion(publicacion: Publicacion): void {
    this.publicacionAbierta.set(publicacion);
    this.biblioteca.recomendar(publicacion.isbn).subscribe({
      next: (recomendaciones) => this.recomendaciones.set(recomendaciones),
    });
  }

  cambiarVista(vista: 'buscar' | 'explorar' | 'guardados'): void {
    this.vista.set(vista);
    this.publicacionAbierta.set(null);
    this.recomendaciones.set([]);

    if (vista === 'buscar') {
      this.seRealizoBusqueda.set(false);
    } else if (vista === 'explorar') {
      this.seRealizoBusqueda.set(true);
      this.explorar('literature');
    } else {
      this.seRealizoBusqueda.set(true);
    }
  }

  explorar(consulta: string): void {
    this.vista.set('explorar');
    this.seRealizoBusqueda.set(true);
    this.estaBuscando.set(true);
    this.error.set('');
    this.biblioteca.buscar(consulta).subscribe({
      next: (publicaciones) => {
        this.publicaciones.set(publicaciones);
        this.estaBuscando.set(false);
      },
      error: () => {
        this.estaBuscando.set(false);
        this.error.set('No fue posible cargar esta categoría.');
      },
    });
  }

  guardarPublicacion(publicacion: Publicacion): void {
    const guardadas = this.publicacionesGuardadas();
    if (guardadas.some((item) => item.isbn === publicacion.isbn)) {
      return;
    }
    const actualizadas = [...guardadas, publicacion];
    this.publicacionesGuardadas.set(actualizadas);
    localStorage.setItem('bibliologos_guardados', JSON.stringify(actualizadas));
  }

  quitarPublicacion(publicacion: Publicacion): void {
    const actualizadas = this.publicacionesGuardadas().filter(
      (item) => item.isbn !== publicacion.isbn,
    );
    this.publicacionesGuardadas.set(actualizadas);
    localStorage.setItem('bibliologos_guardados', JSON.stringify(actualizadas));
  }

  estaGuardada(publicacion: Publicacion): boolean {
    return this.publicacionesGuardadas().some((item) => item.isbn === publicacion.isbn);
  }

  cerrarDetalle(): void {
    this.publicacionAbierta.set(null);
  }
}
