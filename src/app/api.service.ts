//api.service.ts

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
    providedIn: 'root'
})

//Angular holds the "Main Page" while the Express handles
//All of the API stuff
export class ApiService {
    constructor(private http: HttpClient) { }
    forwardGET(path: string) {
        return this.http.get(
            `api/${path}`,
            {responseType: 'json'});
    }
}
