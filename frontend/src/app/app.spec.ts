import { TestBed } from '@angular/core/testing';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import {
  HttpTestingController,
  provideHttpClientTesting,
} from '@angular/common/http/testing';
import { AUTH_TOKEN_KEY } from './core/interceptors/auth.interceptor';
import { authInterceptor } from './core/interceptors/auth.interceptor';
import { App } from './app';

describe('App', () => {
  beforeEach(async () => {
    sessionStorage.clear();
    localStorage.clear();
    await TestBed.configureTestingModule({
      imports: [App],
      providers: [
        provideHttpClient(withInterceptors([authInterceptor])),
        provideHttpClientTesting(),
      ],
    }).compileComponents();
  });

  it('should create the app', () => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;
    expect(app).toBeTruthy();
  });

  it('should ask unauthenticated visitors to sign in', () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('h1')?.textContent).toContain('Iniciar sesión');
  });

  it('should render the welcome title after verifying a reader session', () => {
    sessionStorage.setItem(AUTH_TOKEN_KEY, 'reader-token');
    const fixture = TestBed.createComponent(App);
    const httpTesting = TestBed.inject(HttpTestingController);
    const sessionRequest = httpTesting.expectOne('http://localhost:8000/api/auth/me');
    expect(sessionRequest.request.headers.get('Authorization')).toBe(
      'Bearer reader-token',
    );
    sessionRequest.flush({ username: 'reader', role: 'lector' });
    httpTesting.expectOne('http://localhost:8000/api/estadisticas').flush({
      cantidad: 1,
      calificacion_promedio: 4.5,
      calificacion_mediana: 4.5,
      paginas: 100,
      horas_lectura: 3,
    });

    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('h1')?.textContent).toContain(
      '¿Qué te interesa explorar?',
    );
    expect(compiled.querySelector('.navigation')?.textContent).not.toContain(
      'Mi catálogo',
    );
  });

  it('should load the local catalog for an administrator', () => {
    sessionStorage.setItem(AUTH_TOKEN_KEY, 'admin-token');
    const fixture = TestBed.createComponent(App);
    const httpTesting = TestBed.inject(HttpTestingController);
    httpTesting
      .expectOne('http://localhost:8000/api/auth/me')
      .flush({ username: 'admin', role: 'admin' });
    httpTesting.expectOne('http://localhost:8000/api/estadisticas').flush({
      cantidad: 1,
      calificacion_promedio: 4.5,
      calificacion_mediana: 4.5,
      paginas: 100,
      horas_lectura: 3,
    });

    fixture.componentInstance.cambiarVista('catalogo');
    httpTesting.expectOne('http://localhost:8000/api/catalogo').flush([
      {
        isbn: 'LOCAL-001',
        titulo: 'Libro local',
        autor: 'Autora',
        genero: 'Ficción',
        paginas: 100,
        calificacion: 4.5,
        tipo: 'fisico',
        stock: 2,
        ubicacion: 'Estante A',
      },
    ]);

    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('.management-card h3')?.textContent).toContain(
      'Libro local',
    );
    expect(compiled.querySelector('.management-heading')?.textContent).toContain(
      'se guarda en SQLite',
    );
  });
});
