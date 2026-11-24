import { Component, output } from '@angular/core';

@Component({
  selector: 'app-sidebar',
  imports: [],
  templateUrl: './sidebar.html',
  styleUrl: './sidebar.css',
})
export class Sidebar {
  readonly collapsedChange = output<boolean>();
  readonly navigationChange = output<'buscar' | 'explorar' | 'guardados'>();
  collapsed = false;
  active: 'buscar' | 'explorar' | 'guardados' = 'buscar';

  toggle(): void {
    this.collapsed = !this.collapsed;
    this.collapsedChange.emit(this.collapsed);
  }

  navegar(destination: 'buscar' | 'explorar' | 'guardados'): void {
    this.active = destination;
    this.navigationChange.emit(destination);
  }
}
