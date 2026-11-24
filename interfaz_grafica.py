"""
interfaz_grafica.py
Interfaz Gráfica de Escritorio (GUI) 100% en Python 3 usando tkinter (biblioteca estándar).
No requiere pip install ni librerías externas.
Reutiliza directamente modelos.py, motor_funcional.py, motor_logico.py y main.py.
Ejecución en VS Code: python interfaz_grafica.py
"""

from datetime import datetime
import math
import random
import statistics
import tkinter as tk
from tkinter import messagebox, ttk

from main import cargar_datos_iniciales
from modelos import FabricaPublicaciones, Lector, RepositorioBiblioteca
from motor_funcional import ejecutar_pipeline_analisis
from motor_logico import (
    BaseConocimiento,
    EstrategiaCombinada,
    EstrategiaPorAutor,
    EstrategiaPorGenero,
    recomendar_libros,
    unificar,
)


class AplicacionBibliotecaGUI(tk.Tk):
    """Ventana principal GUI editorial (marfil, tinta oscura y borgoña)."""

    COLOR_MARFIL = "#FAF8F4"
    COLOR_PAPEL = "#FFFFFF"
    COLOR_TINTA = "#1C1917"
    COLOR_BORGONA = "#7F1D2C"

    def __init__(self):
        super().__init__()
        self.title("BiblioLogos — Sistema Gestor y Recomendador Inteligente (GUI)")
        self.geometry("1040x680")
        self.configure(bg=self.COLOR_MARFIL)

        self.repositorio = RepositorioBiblioteca()
        cargar_datos_iniciales(self.repositorio)
        self.base_conocimiento = BaseConocimiento()

        self._configurar_estilos()
        self._construir_cabecera()
        self._construir_pestanas()
        self._refrescar_catalogo()
        self._refrescar_estadisticas()

    def _configurar_estilos(self):
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure("TFrame", background=self.COLOR_MARFIL)
        estilo.configure("TLabel", background=self.COLOR_MARFIL, foreground=self.COLOR_TINTA)
        estilo.configure(
            "Titulo.TLabel",
            background=self.COLOR_MARFIL,
            foreground=self.COLOR_TINTA,
            font=("Georgia", 16, "bold"),
        )
        estilo.configure(
            "Primario.TButton",
            background=self.COLOR_BORGONA,
            foreground="#FFFFFF",
            padding=(12, 6),
        )
        estilo.map("Primario.TButton", background=[("active", "#641420")])

    def _construir_cabecera(self):
        marco = ttk.Frame(self, padding=(16, 12))
        marco.pack(fill="x")
        ttk.Label(
            marco,
            text="BiblioLogos — Sistema Multiparadigma de Libros",
            style="Titulo.TLabel",
        ).pack(side="left")
        ttk.Label(
            marco,
            text="Lenguajes de Programación (100000SI68) · Python 3 Estándar",
        ).pack(side="right")

    def _construir_pestanas(self):
        self.cuaderno = ttk.Notebook(self)
        self.cuaderno.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        self.tab_catalogo = ttk.Frame(self.cuaderno, padding=12)
        self.tab_funcional = ttk.Frame(self.cuaderno, padding=12)
        self.tab_logico = ttk.Frame(self.cuaderno, padding=12)
        self.tab_estadisticas = ttk.Frame(self.cuaderno, padding=12)

        self.cuaderno.add(self.tab_catalogo, text="Catálogo y Registro (POO)")
        self.cuaderno.add(self.tab_funcional, text="Motor Funcional (Unidad 1)")
        self.cuaderno.add(self.tab_logico, text="Motor Lógico (Unidad 2)")
        self.cuaderno.add(self.tab_estadisticas, text="Estadísticas y Sorpresa (Unidad 3)")

        self._construir_tab_catalogo()
        self._construir_tab_funcional()
        self._construir_tab_logico()
        self._construir_tab_estadisticas()

    def _construir_tab_catalogo(self):
        columnas = ("isbn", "titulo", "autor", "genero", "tipo", "paginas", "calif")
        self.tabla_libros = ttk.Treeview(
            self.tab_catalogo, columns=columnas, show="headings", height=11
        )
        encabezados = {
            "isbn": "ISBN",
            "titulo": "Título",
            "autor": "Autor",
            "genero": "Género",
            "tipo": "Tipo",
            "paginas": "Páginas",
            "calif": "Calif.",
        }
        for col, texto in encabezados.items():
            self.tabla_libros.heading(col, text=texto)
            self.tabla_libros.column(col, width=125 if col != "titulo" else 220)
        self.tabla_libros.pack(fill="both", expand=True, pady=(0, 12))

        form = ttk.LabelFrame(
            self.tab_catalogo, text="Registrar Publicación (Patrón Fábrica)", padding=10
        )
        form.pack(fill="x")

        self.var_tipo = tk.StringVar(value="fisico")
        self.var_isbn = tk.StringVar()
        self.var_titulo = tk.StringVar()
        self.var_autor = tk.StringVar()
        self.var_genero = tk.StringVar(value="Realismo Mágico")
        self.var_paginas = tk.StringVar(value="320")
        self.var_calif = tk.StringVar(value="4.6")
        self.var_extra1 = tk.StringVar(value="3")
        self.var_extra2 = tk.StringVar(value="Estante C-01")

        campos = [
            ("Tipo (fisico/ebook):", self.var_tipo),
            ("ISBN:", self.var_isbn),
            ("Título:", self.var_titulo),
            ("Autor:", self.var_autor),
            ("Género:", self.var_genero),
            ("Páginas:", self.var_paginas),
            ("Calificación:", self.var_calif),
            ("Stock / Formato:", self.var_extra1),
            ("Ubicación / Peso MB:", self.var_extra2),
        ]

        for idx, (etiqueta, var) in enumerate(campos):
            fila = idx // 3
            col = (idx % 3) * 2
            ttk.Label(form, text=etiqueta).grid(row=fila, column=col, sticky="w", padx=4, pady=4)
            ttk.Entry(form, textvariable=var, width=20).grid(
                row=fila, column=col + 1, sticky="ew", padx=4, pady=4
            )

        ttk.Button(
            form,
            text="Agregar al Catálogo",
            style="Primario.TButton",
            command=self._agregar_publicacion_gui,
        ).grid(row=3, column=0, columnspan=2, sticky="w", padx=4, pady=(8, 0))

    def _agregar_publicacion_gui(self):
        try:
            tipo = self.var_tipo.get().strip().lower()
            datos_base = {
                "isbn": self.var_isbn.get(),
                "titulo": self.var_titulo.get(),
                "autor": self.var_autor.get(),
                "genero": self.var_genero.get(),
                "paginas": int(self.var_paginas.get()),
                "calificacion": float(self.var_calif.get()),
            }
            if tipo == "fisico":
                datos_base["stock"] = int(self.var_extra1.get())
                datos_base["ubicacion"] = self.var_extra2.get()
            else:
                datos_base["formato"] = self.var_extra1.get()
                datos_base["peso_mb"] = float(self.var_extra2.get())

            nueva = FabricaPublicaciones.crear_publicacion(tipo, **datos_base)
            self.repositorio.agregar_publicacion(nueva)
            self._refrescar_catalogo()
            self._refrescar_estadisticas()
            self.var_isbn.set("")
            self.var_titulo.set("")
            self.var_autor.set("")
            messagebox.showinfo("Registro exitoso", f"Se agregó: {nueva.titulo}")
        except ValueError as error:
            messagebox.showerror("Error de validación", str(error))

    def _refrescar_catalogo(self):
        for item in self.tabla_libros.get_children():
            self.tabla_libros.delete(item)
        for libro in self.repositorio.obtener_lista_catalogo():
            tipo = "Físico" if hasattr(libro, "stock") else "Ebook"
            self.tabla_libros.insert(
                "",
                "end",
                values=(
                    libro.isbn,
                    libro.titulo,
                    libro.autor,
                    libro.genero,
                    tipo,
                    libro.paginas,
                    f"{libro.calificacion:.1f}",
                ),
            )

    def _construir_tab_funcional(self):
        controles = ttk.Frame(self.tab_funcional)
        controles.pack(fill="x", pady=(0, 10))

        self.var_genero_filtro = tk.StringVar(value="todos")
        self.var_calif_min = tk.DoubleVar(value=4.5)

        ttk.Label(controles, text="Género:").pack(side="left", padx=(0, 6))
        ttk.Entry(controles, textvariable=self.var_genero_filtro, width=22).pack(
            side="left", padx=(0, 14)
        )
        ttk.Label(controles, text="Calificación mínima:").pack(side="left", padx=(0, 6))
        ttk.Spinbox(
            controles, from_=0.0, to=5.0, increment=0.1, textvariable=self.var_calif_min, width=6
        ).pack(side="left", padx=(0, 14))
        ttk.Button(
            controles,
            text="Ejecutar Pipeline (filter -> map -> reduce)",
            style="Primario.TButton",
            command=self._ejecutar_pipeline_gui,
        ).pack(side="left")

        self.salida_funcional = tk.Text(
            self.tab_funcional, height=22, font=("Courier New", 10), bg=self.COLOR_PAPEL
        )
        self.salida_funcional.pack(fill="both", expand=True)

    def _ejecutar_pipeline_gui(self):
        catalogo = self.repositorio.obtener_lista_catalogo()
        res = ejecutar_pipeline_analisis(
            catalogo, self.var_genero_filtro.get(), self.var_calif_min.get()
        )
        self.salida_funcional.delete("1.0", tk.END)
        self.salida_funcional.insert(
            tk.END,
            f"PIPELINE FUNCIONAL PURO (sin mutar catálogo original de {res['cantidad_original']} libros)\n"
            + "-" * 72
            + "\n",
        )
        for isbn, titulo, horas in res["tiempos_por_libro"]:
            self.salida_funcional.insert(tk.END, f" • [{isbn}] {titulo} -> {horas:.2f} h\n")
        self.salida_funcional.insert(
            tk.END,
            f"\nTotal acumulado de páginas (reduce): {res['total_paginas']} pág.\n"
            f"Horas estimadas exactas / ceil: {res['horas_exactas']} h / {res['horas_redondeadas']} h\n",
        )

    def _construir_tab_logico(self):
        barra = ttk.Frame(self.tab_logico)
        barra.pack(fill="x", pady=(0, 10))

        self.var_lector_sel = tk.StringVar(value="LEC-001")
        self.var_estrategia = tk.StringVar(value="combinada")
        self.var_corte = tk.BooleanVar(value=False)

        ttk.Label(barra, text="Código Lector:").pack(side="left", padx=(0, 6))
        ttk.Entry(barra, textvariable=self.var_lector_sel, width=12).pack(side="left", padx=(0, 12))
        ttk.Label(barra, text="Estrategia:").pack(side="left", padx=(0, 6))
        ttk.Combobox(
            barra,
            textvariable=self.var_estrategia,
            values=("combinada", "genero", "autor"),
            state="readonly",
            width=14,
        ).pack(side="left", padx=(0, 12))
        ttk.Checkbutton(barra, text="Activar Corte (!)", variable=self.var_corte).pack(
            side="left", padx=(0, 12)
        )
        ttk.Button(
            barra,
            text="Inferir Recomendaciones",
            style="Primario.TButton",
            command=self._ejecutar_recomendador_gui,
        ).pack(side="left")

        self.salida_logica = tk.Text(
            self.tab_logico, height=22, font=("Courier New", 10), bg=self.COLOR_PAPEL
        )
        self.salida_logica.pack(fill="both", expand=True)

    def _ejecutar_recomendador_gui(self):
        catalogo = self.repositorio.obtener_lista_catalogo()
        lectores = self.repositorio.obtener_lista_lectores()
        self.base_conocimiento.cargar_desde_repositorio(catalogo, lectores)

        lector = self.repositorio.buscar_lector_por_codigo(self.var_lector_sel.get())
        self.salida_logica.delete("1.0", tk.END)
        if lector is None:
            self.salida_logica.insert(tk.END, "No se encontró el lector indicado.\n")
            return

        mapa_est = {
            "combinada": EstrategiaCombinada(),
            "genero": EstrategiaPorGenero(),
            "autor": EstrategiaPorAutor(),
        }
        estrategia = mapa_est.get(self.var_estrategia.get(), EstrategiaCombinada())
        recs = recomendar_libros(
            lector, self.base_conocimiento, catalogo, corte=self.var_corte.get(), estrategia=estrategia
        )

        modo = "CORTE (!)" if self.var_corte.get() else "BACKTRACKING (todas)"
        self.salida_logica.insert(
            tk.END,
            f"Lector: {lector.nombre} | {estrategia.nombre} | Modo: {modo}\n" + "-" * 72 + "\n",
        )
        if len(recs) == 0:
            self.salida_logica.insert(tk.END, "Sin nuevas recomendaciones deducidas.\n")
        else:
            for i, rec in enumerate(recs, start=1):
                self.salida_logica.insert(
                    tk.END,
                    f"{i}. {rec['libro'].mostrar_info()}\n"
                    f"   Motivos: {' ; '.join(rec['motivos'])} | Afinidad: {rec['puntaje_afinidad']}\n\n",
                )

        exito, lig, msg = unificar("AutorX", "Gabriel García Márquez")
        self.salida_logica.insert(tk.END, f"Demo unificar('AutorX', 'Gabriel García Márquez') -> {exito} {lig} ({msg})\n")

    def _construir_tab_estadisticas(self):
        self.texto_stats = tk.Text(
            self.tab_estadisticas, height=16, font=("Courier New", 11), bg=self.COLOR_PAPEL
        )
        self.texto_stats.pack(fill="both", expand=True, pady=(0, 10))
        ttk.Button(
            self.tab_estadisticas,
            text="Actualizar Estadísticas y Sortear Libro Sorpresa",
            style="Primario.TButton",
            command=self._refrescar_estadisticas,
        ).pack(anchor="w")

    def _refrescar_estadisticas(self):
        catalogo = self.repositorio.obtener_lista_catalogo()
        self.texto_stats.delete("1.0", tk.END)
        if len(catalogo) == 0:
            self.texto_stats.insert(tk.END, "Catálogo vacío.")
            return

        califs = [l.calificacion for l in catalogo]
        promedio = statistics.mean(califs)
        mediana = statistics.median(califs)
        paginas = sum(l.paginas for l in catalogo)
        horas_ceil = math.ceil(paginas / 40.0)
        sorpresa = random.choice(catalogo)
        codigo_prest = f"PREST-{random.randint(1000, 9999)}"
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

        resumen = (
            f"REPORTE ESTADÍSTICO DEL CATÁLOGO  |  {fecha}\n"
            f"{'=' * 64}\n"
            f"Publicaciones totales  : {len(catalogo)}\n"
            f"Promedio calificación  : {promedio:.2f} / 5.00\n"
            f"Mediana calificación   : {mediana:.2f} / 5.00\n"
            f"Total de páginas       : {paginas} pág.\n"
            f"Tiempo estimado (ceil) : {horas_ceil} horas\n\n"
            f"LIBRO SORPRESA DEL DÍA (random.choice)\n"
            f"-> {sorpresa.mostrar_info()}\n"
            f"Código sugerido de préstamo: {codigo_prest}\n"
        )
        self.texto_stats.insert(tk.END, resumen)


if __name__ == "__main__":
    app = AplicacionBibliotecaGUI()
    app.mainloop()
