import { HttpClient } from '@angular/common/http';
import { Injectable, inject, signal } from '@angular/core';
import { Observable, catchError, finalize, of, tap, throwError } from 'rxjs';
import { AUTH_TOKEN_KEY } from '../interceptors/auth.interceptor';
import { UsuarioAutenticado } from '../models/library.models';

export interface RespuestaSesion extends UsuarioAutenticado {
  access_token: string;
  token_type: 'bearer';
  expires_in: number;
}

@Injectable({ providedIn: 'root' })
export class ServicioAutenticacion {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = 'http://localhost:8000/api/auth';

  readonly usuario = signal<UsuarioAutenticado | null>(null);
  readonly cargando = signal(true);

  get token(): string | null {
    return sessionStorage.getItem(AUTH_TOKEN_KEY);
  }

  restaurarSesion(): Observable<UsuarioAutenticado | null> {
    const token = this.token;
    if (!token) {
      this.cargando.set(false);
      return of(null);
    }

    return this.http
      .get<UsuarioAutenticado>(`${this.apiUrl}/me`)
      .pipe(
        tap((usuario) => this.usuario.set(usuario)),
        catchError((error: unknown) => {
          this.limpiarSesion();
          return throwError(() => error);
        }),
        finalize(() => this.cargando.set(false)),
      );
  }

  iniciarSesion(username: string, password: string): Observable<UsuarioAutenticado> {
    return this.http
      .post<RespuestaSesion>(`${this.apiUrl}/login`, { username, password })
      .pipe(tap((sesion) => this.establecerSesion(sesion)));
  }

  registrarLector(username: string, password: string): Observable<UsuarioAutenticado> {
    return this.http
      .post<RespuestaSesion>(`${this.apiUrl}/register`, { username, password })
      .pipe(tap((sesion) => this.establecerSesion(sesion)));
  }

  cerrarSesion(): Observable<void> {
    if (!this.token) {
      this.limpiarSesion();
      return of(undefined);
    }
    return this.http.post<void>(`${this.apiUrl}/logout`, {}).pipe(
      finalize(() => this.limpiarSesion()),
    );
  }

  private establecerSesion(sesion: RespuestaSesion): void {
    sessionStorage.setItem(AUTH_TOKEN_KEY, sesion.access_token);
    this.usuario.set({ username: sesion.username, role: sesion.role });
    this.cargando.set(false);
  }

  private limpiarSesion(): void {
    sessionStorage.removeItem(AUTH_TOKEN_KEY);
    this.usuario.set(null);
  }
}
