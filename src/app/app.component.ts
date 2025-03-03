import { Component, OnInit } from '@angular/core';
import { ApiService } from './api.service';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})

export class AppComponent implements OnInit {
  title = 'worldbricks';
  message: any;
  constructor(private apiService: ApiService) {};
  ngOnInit() {
      console.log("Made it to OnInit function");
      this.apiService.forwardGET('67c0a8171abe9aa514aadf4e/info').subscribe(data => {
        this.message = data;
      })
  }
}
