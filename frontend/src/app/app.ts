import { HttpErrorResponse } from '@angular/common/http';
import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { TarjetaPublicacion } from './components/publication-card/publication-card';
import { BarraBusqueda } from './components/search-bar/search-bar';
import { Sidebar } from './components/sidebar/sidebar';
import { ServicioBiblioteca } from './core/services/library.service';
import {
  DatosPublicacion,
  EstadisticasBiblioteca,
  Publicacion,
  Recomendacion,
} from './core/models/library.models';

interface FormularioPublicacion {
  isbn: string;
  titulo: string;
  autor: string;
  genero: string;
  paginas: number;
  calificacion: number;
  tipo: 'fisico' | 'ebook';
  stock: number;
  ubicacion: string;
  formato: string;
  peso_mb: number;
}

@Component({
  selector: 'app-root',
  imports: [FormsModule, Sidebar, BarraBusqueda, TarjetaPublicacion],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  private readonly biblioteca = inject(ServicioBiblioteca);

  readonly barraLateralOculta = signal(false);
  readonly seRealizoBusqueda = signal(false);
  readonly estaBuscando = signal(false);
  readonly error = signal('');
  readonly formularioAbierto = signal(false);
  readonly guardandoFormulario = signal(false);
  readonly isbnEditando = signal<string | null>(null);
  readonly publicaciones = signal<Publicacion[]>([]);
  readonly recomendaciones = signal<Recomendacion[]>([]);
  readonly estadisticas = signal<EstadisticasBiblioteca | null>(null);
  readonly vista = signal<'buscar' | 'explorar' | 'guardados' | 'catalogo'>('buscar');
  formulario: FormularioPublicacion = this.formularioVacio();
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

  cambiarVista(
    vista: 'buscar' | 'explorar' | 'guardados' | 'catalogo',
  ): void {
    this.vista.set(vista);
    this.publicacionAbierta.set(null);
    this.recomendaciones.set([]);
    this.error.set('');

    if (vista === 'buscar') {
      this.seRealizoBusqueda.set(false);
    } else if (vista === 'explorar') {
      this.seRealizoBusqueda.set(true);
      this.explorar('literature');
    } else if (vista === 'catalogo') {
      this.seRealizoBusqueda.set(true);
      this.cargarCatalogo();
    } else {
      this.seRealizoBusqueda.set(true);
    }
  }

  cargarCatalogo(): void {
    this.estaBuscando.set(true);
    this.biblioteca.listarCatalogo().subscribe({
      next: (publicaciones) => {
        this.publicaciones.set(publicaciones);
        this.estaBuscando.set(false);
      },
      error: (error: unknown) => {
        this.estaBuscando.set(false);
        this.error.set(
          this.mensajeError(error, 'No fue posible cargar el catálogo local.'),
        );
      },
    });
  }

  abrirFormulario(publicacion?: Publicacion): void {
    this.error.set('');
    this.isbnEditando.set(publicacion?.isbn ?? null);
    this.formulario = publicacion
      ? {
          isbn: publicacion.isbn,
          titulo: publicacion.titulo,
          autor: publicacion.autor,
          genero: publicacion.genero,
          paginas: publicacion.paginas,
          calificacion: publicacion.calificacion,
          tipo: publicacion.tipo,
          stock: publicacion.stock ?? 0,
          ubicacion: publicacion.ubicacion ?? '',
          formato: publicacion.formato ?? 'EPUB',
          peso_mb: publicacion.peso_mb ?? 1,
        }
      : this.formularioVacio();
    this.formularioAbierto.set(true);
  }

  cerrarFormulario(): void {
    if (!this.guardandoFormulario()) {
      this.formularioAbierto.set(false);
    }
  }

  guardarFormulario(): void {
    const form = this.formulario;
    const datos: DatosPublicacion = {
      isbn: form.isbn.trim(),
      titulo: form.titulo.trim(),
      autor: form.autor.trim(),
      genero: form.genero.trim(),
      paginas: Number(form.paginas),
      calificacion: Number(form.calificacion),
      tipo: form.tipo,
      ...(form.tipo === 'fisico'
        ? { stock: Number(form.stock), ubicacion: form.ubicacion.trim() }
        : { formato: form.formato, peso_mb: Number(form.peso_mb) }),
    };

    this.error.set('');
    this.guardandoFormulario.set(true);
    const isbnOriginal = this.isbnEditando();
    const solicitud = isbnOriginal
      ? this.biblioteca.actualizarPublicacion(isbnOriginal, datos)
      : this.biblioteca.crearPublicacion(datos);

    solicitud.subscribe({
      next: () => {
        this.guardandoFormulario.set(false);
        this.formularioAbierto.set(false);
        this.cargarCatalogo();
        this.cargarEstadisticas();
      },
      error: (error: unknown) => {
        this.guardandoFormulario.set(false);
        this.error.set(
          this.mensajeError(error, 'No fue posible guardar la publicación.'),
        );
      },
    });
  }

  eliminarDelCatalogo(publicacion: Publicacion): void {
    if (!window.confirm(`¿Eliminar "${publicacion.titulo}" del catálogo local?`)) {
      return;
    }
    this.error.set('');
    this.estaBuscando.set(true);
    this.biblioteca.eliminarPublicacion(publicacion.isbn).subscribe({
      next: () => {
        this.cargarCatalogo();
        this.cargarEstadisticas();
      },
      error: (error: unknown) => {
        this.estaBuscando.set(false);
        this.error.set(
          this.mensajeError(error, 'No fue posible eliminar la publicación.'),
        );
      },
    });
  }

  private formularioVacio(): FormularioPublicacion {
    return {
      isbn: '',
      titulo: '',
      autor: '',
      genero: '',
      paginas: 1,
      calificacion: 0,
      tipo: 'fisico',
      stock: 0,
      ubicacion: '',
      formato: 'EPUB',
      peso_mb: 1,
    };
  }

  private mensajeError(error: unknown, fallback: string): string {
    if (error instanceof HttpErrorResponse) {
      const payload: unknown = error.error;
      if (
        typeof payload === 'object' &&
        payload !== null &&
        'detail' in payload
      ) {
        const detail: unknown = payload.detail;
        if (typeof detail === 'string') {
          return detail;
        }
        if (Array.isArray(detail)) {
          const messages = detail
            .map((item: unknown) => {
              if (
                typeof item === 'object' &&
                item !== null &&
                'msg' in item &&
                typeof item.msg === 'string'
              ) {
                return item.msg;
              }
              return '';
            })
            .filter(Boolean);
          if (messages.length > 0) {
            return messages.join(' ');
          }
        }
      }
    }
    return fallback;
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
