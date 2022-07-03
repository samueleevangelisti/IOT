import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor
} from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable()
export class ProxyInterceptor implements HttpInterceptor {

  constructor() {}

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    let handleRequest = new HttpRequest('POST', `${environment.baseUrl}/proxy`, {
      method: request.method,
      url: request.url,
      body: request.body
    })    
    return next.handle(handleRequest);
  }
}
