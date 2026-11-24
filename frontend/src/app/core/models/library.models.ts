export interface Publicacion {
  isbn: string;
  titulo: string;
  autor: string;
  genero: string;
  paginas: number;
  calificacion: number;
  tipo: 'fisico' | 'ebook';
  formato?: string;
  ubicacion?: string;
  stock?: number;
  peso_mb?: number;
  portada_url?: string;
  enlace_abierto?: string;
  descripcion?: string;
  etiquetas?: string[];
}

export interface Recomendacion {
  publicacion: Publicacion;
  puntaje: number;
  motivos: string[];
}

export interface EstadisticasBiblioteca {
  cantidad: number;
  calificacion_promedio: number;
  calificacion_mediana: number;
  paginas: number;
  horas_lectura: number;
}
