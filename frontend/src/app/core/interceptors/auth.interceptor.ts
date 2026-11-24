import { HttpInterceptorFn } from '@angular/common/http';

export const AUTH_TOKEN_KEY = 'bibliologos_access_token';

export const authInterceptor: HttpInterceptorFn = (request, next) => {
  const token = sessionStorage.getItem(AUTH_TOKEN_KEY);
  if (!token || !request.url.startsWith('http://localhost:8000/api/')) {
    return next(request);
  }
  return next(
    request.clone({
      setHeaders: { Authorization: `Bearer ${token}` },
    }),
  );
};
