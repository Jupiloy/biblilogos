"""
motor_logico.py
Unidad 2: Programación Lógica simulada en Python 3.
Incluye Base de Conocimiento declarativa (hechos), unificación lógica,
recursividad estilo Prolog [Cabeza | Cola], motor de inferencia con
backtracking / corte (!) y Patrón de Diseño Estrategia en español.
100% Python 3 — Biblioteca Estándar.
"""

from abc import ABC, abstractmethod


# ==============================================================================
# [Unidad 2 - Base de Conocimiento Declarativa (Hechos)]
# Modela predicados: es_autor(libro, autor), es_genero(libro, genero),
# le_gusta(lector, libro) mediante diccionarios y listas.
# ==============================================================================

class BaseConocimiento:
    """Almacena los hechos declarativos sobre libros y preferencias de lectores."""

    def __init__(self):
        self.hechos_es_autor = {}
        self.hechos_es_genero = {}
        self.hechos_le_gusta = {}

    def cargar_desde_repositorio(self, catalogo, lectores):
        """Sincroniza los hechos lógicos a partir del catálogo y los lectores."""
        self.hechos_es_autor = {}
        self.hechos_es_genero = {}
        self.hechos_le_gusta = {}

        for libro in catalogo:
            self.hechos_es_autor[libro.isbn] = libro.autor
            self.hechos_es_genero[libro.isbn] = libro.genero

        for lector in lectores:
            self.hechos_le_gusta[lector.codigo] = list(lector.libros_leidos)

    def es_autor(self, isbn_libro):
        """Consulta el hecho es_autor(Libro, Autor)."""
        return self.hechos_es_autor.get(isbn_libro)

    def es_genero(self, isbn_libro):
        """Consulta el hecho es_genero(Libro, Genero)."""
        return self.hechos_es_genero.get(isbn_libro)

    def le_gusta(self, codigo_lector):
        """Consulta los hechos le_gusta(Lector, Libro)."""
        return list(self.hechos_le_gusta.get(codigo_lector, []))


# ==============================================================================
# [Unidad 2 - Simulación de Unificación Lógica]
# Variables lógicas: inician con letra mayúscula y sin espacios (ej. Autor, X).
# ==============================================================================

def _es_variable_logica(termino):
    """Determina si un término sigue la convención Prolog de variable lógica."""
    texto = str(termino).strip()
    return len(texto) > 0 and texto[0].isupper() and (" " not in texto)


def unificar(termino1, termino2):
    """
    Simula la unificación lógica entre dos términos.
    Retorna una tupla (exito: bool, ligaduras: dict, mensaje: str).
    """
    t1 = str(termino1).strip()
    t2 = str(termino2).strip()

    if len(t1) == 0 or len(t2) == 0:
        return (False, {}, "Fallo: ambos términos deben ser no vacíos.")

    if t1 == t2:
        return (True, {}, f"Unificación exitosa: constantes idénticas ('{t1}').")

    es_var1 = _es_variable_logica(t1)
    es_var2 = _es_variable_logica(t2)

    if es_var1 and not es_var2:
        return (True, {t1: t2}, f"Variable '{t1}' unificada con constante '{t2}'.")

    if es_var2 and not es_var1:
        return (True, {t2: t1}, f"Variable '{t2}' unificada con constante '{t1}'.")

    if es_var1 and es_var2:
        return (True, {t1: t2}, f"Variables '{t1}' y '{t2}' enlazadas entre sí.")

    return (
        False,
        {},
        f"Fallo de unificación: las constantes '{t1}' y '{t2}' no coinciden.",
    )


# ==============================================================================
# [Unidad 2 - Recursividad estilo Prolog: Patrón [Cabeza | Cola]]
# Caso base: lista vacía -> False.
# Caso recursivo: compara Cabeza (lista[0]) y recurre sobre Cola (lista[1:]).
# ==============================================================================

def existe_en_lista(elemento, lista):
    """Verifica recursivamente si elemento pertenece a lista usando [Cabeza | Cola]."""
    if len(lista) == 0:
        return False

    cabeza = lista[0]
    cola = lista[1:]

    if cabeza == elemento:
        return True

    return existe_en_lista(elemento, cola)


# ==============================================================================
# [Patrón de Diseño de Comportamiento - Estrategia (Strategy)]
# Permite intercambiar dinámicamente la regla de inferencia de recomendaciones.
# ==============================================================================

class EstrategiaRecomendacion(ABC):
    """Interfaz base para las estrategias lógicas de recomendación."""

    @property
    @abstractmethod
    def nombre(self):
        raise NotImplementedError("Subclase debe definir el nombre de estrategia.")

    @abstractmethod
    def evaluar_candidato(self, isbn_candidato, autores_gustados, generos_gustados, base):
        """Retorna lista de motivos deducidos y puntaje de afinidad lógica."""
        raise NotImplementedError("Subclase debe implementar evaluar_candidato.")


class EstrategiaPorGenero(EstrategiaRecomendacion):
    """Deduce recomendaciones únicamente cuando coincide es_genero(Libro, G)."""

    @property
    def nombre(self):
        return "EstrategiaPorGenero"

    def evaluar_candidato(self, isbn_candidato, autores_gustados, generos_gustados, base):
        genero_candidato = base.es_genero(isbn_candidato)
        for genero_fav in generos_gustados:
            exito, _, _ = unificar(genero_candidato, genero_fav)
            if exito:
                return ([f"Mismo género de interés ({genero_candidato})"], 1.2)
        return ([], 0.0)


class EstrategiaPorAutor(EstrategiaRecomendacion):
    """Deduce recomendaciones únicamente cuando coincide es_autor(Libro, A)."""

    @property
    def nombre(self):
        return "EstrategiaPorAutor"

    def evaluar_candidato(self, isbn_candidato, autores_gustados, generos_gustados, base):
        autor_candidato = base.es_autor(isbn_candidato)
        for autor_fav in autores_gustados:
            exito, _, _ = unificar(autor_candidato, autor_fav)
            if exito:
                return ([f"Mismo autor predilecto ({autor_candidato})"], 2.0)
        return ([], 0.0)


class EstrategiaCombinada(EstrategiaRecomendacion):
    """Deduce recomendaciones combinando reglas de es_autor y es_genero."""

    @property
    def nombre(self):
        return "EstrategiaCombinada (Autor + Género)"

    def evaluar_candidato(self, isbn_candidato, autores_gustados, generos_gustados, base):
        motivos = []
        puntaje = 0.0

        autor_candidato = base.es_autor(isbn_candidato)
        for autor_fav in autores_gustados:
            exito, _, _ = unificar(autor_candidato, autor_fav)
            if exito:
                motivos.append(f"Mismo autor predilecto ({autor_candidato})")
                puntaje += 2.0
                break

        genero_candidato = base.es_genero(isbn_candidato)
        for genero_fav in generos_gustados:
            exito, _, _ = unificar(genero_candidato, genero_fav)
            if exito:
                motivos.append(f"Mismo género de interés ({genero_candidato})")
                puntaje += 1.2
                break

        return (motivos, puntaje)


# ==============================================================================
# [Unidad 2 - Motor de Inferencia con Indeterminismo (Backtracking) y Corte (!)]
# ==============================================================================

def recomendar_libros(lector, base_conocimiento, catalogo, corte=False, estrategia=None):
    """
    Motor de inferencia declarativo:
    - Obtiene libros que le gustan al lector (hecho le_gusta).
    - Deduce autores y géneros de interés mediante la Base de Conocimiento.
    - Excluye libros ya leídos utilizando existe_en_lista() [Cabeza | Cola].
    - Si corte=False: simula backtracking devolviendo TODAS las soluciones.
    - Si corte=True: simula el operador corte (!) devolviendo solo la primera mejor.
    """
    estrategia_activa = estrategia if estrategia is not None else EstrategiaCombinada()
    libros_leidos = base_conocimiento.le_gusta(lector.codigo)

    autores_gustados = []
    generos_gustados = []

    for isbn_leido in libros_leidos:
        autor = base_conocimiento.es_autor(isbn_leido)
        genero = base_conocimiento.es_genero(isbn_leido)
        if autor and not existe_en_lista(autor, autores_gustados):
            autores_gustados.append(autor)
        if genero and not existe_en_lista(genero, generos_gustados):
            generos_gustados.append(genero)

    soluciones = []

    # Exploración de soluciones (indeterminismo / backtracking)
    for libro in catalogo:
        if existe_en_lista(libro.isbn, libros_leidos):
            continue

        motivos, bono_logico = estrategia_activa.evaluar_candidato(
            libro.isbn, autores_gustados, generos_gustados, base_conocimiento
        )

        if len(motivos) > 0:
            soluciones.append(
                {
                    "libro": libro,
                    "motivos": motivos,
                    "estrategia": estrategia_activa.nombre,
                    "puntaje_afinidad": round(libro.calificacion + bono_logico, 2),
                }
            )

    soluciones.sort(
        key=lambda item: (item["puntaje_afinidad"], item["libro"].calificacion),
        reverse=True,
    )

    # [Unidad 2 - Operador Corte (!)]: detiene la búsqueda tras la primera mejor solución
    if corte and len(soluciones) > 0:
        return [soluciones[0]]

    return soluciones
