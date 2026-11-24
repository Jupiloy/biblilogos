"""
modelos.py
Unidad 3: Programación Orientada a Objetos, Herencia, Validación de Cadenas
y Patrones de Diseño (Fábrica y Repositorio Singleton).
Curso: Lenguajes de Programación (100000SI68)
100% Python 3 — Biblioteca Estándar.
"""

# ==============================================================================
# [Unidad 3 - Validación y normalización de cadenas]
# Uso explícito de .strip(), .lower(), .upper(), len() y operador in
# ==============================================================================

CATEGORIAS_VALIDAS = ("VIP", "FRECUENTE", "GENERAL")


def validar_nombre(nombre):
    """Valida que el nombre no esté vacío tras eliminar espacios laterales."""
    nombre_limpio = str(nombre).strip()
    if len(nombre_limpio) == 0:
        raise ValueError("El nombre no puede estar vacío.")
    if len(nombre_limpio) < 3:
        raise ValueError("El nombre debe tener al menos 3 caracteres.")
    return nombre_limpio


def validar_correo(correo):
    """
    Valida que el correo contenga '@', un '.' posterior a '@' y no tenga espacios.
    Normaliza el resultado en minúsculas.
    """
    correo_limpio = str(correo).strip().lower()
    if len(correo_limpio) == 0:
        raise ValueError("El correo electrónico no puede estar vacío.")
    if " " in correo_limpio:
        raise ValueError("El correo electrónico no debe contener espacios.")
    if "@" not in correo_limpio:
        raise ValueError("El correo electrónico debe contener el símbolo '@'.")

    partes = correo_limpio.split("@")
    if len(partes) != 2 or len(partes[0]) == 0 or len(partes[1]) == 0:
        raise ValueError("Formato de correo electrónico inválido.")

    dominio = partes[1]
    if "." not in dominio or dominio.startswith(".") or dominio.endswith("."):
        raise ValueError("El correo debe incluir un punto válido después de '@'.")

    return correo_limpio


def normalizar_categoria(categoria):
    """Normaliza la categoría de lector a mayúsculas y valida su pertenencia."""
    categoria_normalizada = str(categoria).strip().upper()
    if categoria_normalizada not in CATEGORIAS_VALIDAS:
        raise ValueError(
            "Categoría inválida. Debe ser una de: " + ", ".join(CATEGORIAS_VALIDAS)
        )
    return categoria_normalizada


# ==============================================================================
# [Unidad 3 - POO: Clase Base, Herencia Simple y Sobrescritura de Métodos]
# ==============================================================================

class Publicacion:
    """Clase base que modela una publicación bibliográfica."""

    def __init__(self, isbn, titulo, autor, genero, paginas, calificacion):
        isbn_limpio = str(isbn).strip()
        titulo_limpio = str(titulo).strip()
        autor_limpio = str(autor).strip()
        genero_limpio = str(genero).strip()

        if len(isbn_limpio) < 4:
            raise ValueError("El ISBN debe tener al menos 4 caracteres.")
        if len(titulo_limpio) == 0 or len(autor_limpio) == 0 or len(genero_limpio) == 0:
            raise ValueError("Título, autor y género son obligatorios.")
        if int(paginas) <= 0:
            raise ValueError("El número de páginas debe ser mayor que cero.")
        if not (0.0 <= float(calificacion) <= 5.0):
            raise ValueError("La calificación debe estar comprendida entre 0.0 y 5.0.")

        self.isbn = isbn_limpio
        self.titulo = titulo_limpio
        self.autor = autor_limpio
        self.genero = genero_limpio
        self.paginas = int(paginas)
        self.calificacion = round(float(calificacion), 2)

    def obtener_ficha_inmutable(self):
        """[Unidad 3 - Tupla inmutable] Devuelve la ficha fija (isbn, titulo, autor)."""
        return (self.isbn, self.titulo, self.autor)

    def mostrar_info(self):
        """Método base que retorna una descripción legible de la publicación."""
        return (
            f"[{self.isbn}] '{self.titulo}' - {self.autor} | "
            f"Género: {self.genero} | {self.paginas} pág. | "
            f"Calificación: {self.calificacion:.1f}/5.0"
        )


class LibroFisico(Publicacion):
    """[Unidad 3 - Herencia simple y sobrescritura] Publicación en formato impreso."""

    def __init__(self, isbn, titulo, autor, genero, paginas, calificacion, stock, ubicacion):
        super().__init__(isbn, titulo, autor, genero, paginas, calificacion)
        if int(stock) < 0:
            raise ValueError("El stock no puede ser negativo.")
        ubicacion_limpia = str(ubicacion).strip()
        if len(ubicacion_limpia) == 0:
            raise ValueError("La ubicación en estantería es obligatoria.")

        self.stock = int(stock)
        self.ubicacion = ubicacion_limpia

    def mostrar_info(self):
        """Sobrescribe mostrar_info() agregando stock y ubicación física."""
        info_base = super().mostrar_info()
        return f"{info_base} | [FÍSICO] Stock: {self.stock} | Ubicación: {self.ubicacion}"


class Ebook(Publicacion):
    """[Unidad 3 - Herencia simple y sobrescritura] Publicación en formato digital."""

    FORMATOS_PERMITIDOS = ("PDF", "EPUB")

    def __init__(self, isbn, titulo, autor, genero, paginas, calificacion, formato, peso_mb):
        super().__init__(isbn, titulo, autor, genero, paginas, calificacion)
        formato_normalizado = str(formato).strip().upper()
        if formato_normalizado not in self.FORMATOS_PERMITIDOS:
            raise ValueError("El formato del Ebook debe ser PDF o EPUB.")
        if float(peso_mb) <= 0:
            raise ValueError("El peso en MB debe ser mayor que cero.")

        self.formato = formato_normalizado
        self.peso_mb = round(float(peso_mb), 2)

    def mostrar_info(self):
        """Sobrescribe mostrar_info() agregando formato digital y peso en MB."""
        info_base = super().mostrar_info()
        return f"{info_base} | [EBOOK] Formato: {self.formato} | Peso: {self.peso_mb:.1f} MB"


class Lector:
    """[Unidad 3 - POO + Validación de cadenas] Modela a un lector de la biblioteca."""

    def __init__(self, codigo, nombre, correo, categoria, libros_leidos=None):
        codigo_limpio = str(codigo).strip().upper()
        if len(codigo_limpio) == 0:
            raise ValueError("El código del lector es obligatorio.")

        self.codigo = codigo_limpio
        self.nombre = validar_nombre(nombre)
        self.correo = validar_correo(correo)
        self.categoria = normalizar_categoria(categoria)
        self.libros_leidos = list(libros_leidos) if libros_leidos is not None else []

    def registrar_lectura(self, isbn):
        """Agrega un ISBN a la lista de libros leídos evitando duplicados."""
        isbn_limpio = str(isbn).strip()
        if isbn_limpio not in self.libros_leidos:
            self.libros_leidos.append(isbn_limpio)

    def mostrar_info(self):
        """Devuelve un resumen estructurado del lector."""
        return (
            f"[{self.codigo}] {self.nombre} ({self.categoria}) | "
            f"Correo: {self.correo} | Libros leídos: {len(self.libros_leidos)}"
        )


# ==============================================================================
# [Patrón de Diseño Creacional - Fábrica (Factory Method)]
# Centraliza la creación de LibroFisico y Ebook sin acoplar al cliente
# ==============================================================================

class FabricaPublicaciones:
    """Fábrica encargada de instanciar subclases de Publicacion según el tipo."""

    @staticmethod
    def crear_publicacion(tipo, **datos):
        tipo_normalizado = str(tipo).strip().lower()
        if tipo_normalizado == "fisico":
            return LibroFisico(
                isbn=datos["isbn"],
                titulo=datos["titulo"],
                autor=datos["autor"],
                genero=datos["genero"],
                paginas=datos["paginas"],
                calificacion=datos["calificacion"],
                stock=datos["stock"],
                ubicacion=datos["ubicacion"],
            )
        if tipo_normalizado == "ebook":
            return Ebook(
                isbn=datos["isbn"],
                titulo=datos["titulo"],
                autor=datos["autor"],
                genero=datos["genero"],
                paginas=datos["paginas"],
                calificacion=datos["calificacion"],
                formato=datos["formato"],
                peso_mb=datos["peso_mb"],
            )
        raise ValueError("Tipo de publicación desconocido. Use 'fisico' o 'ebook'.")


# ==============================================================================
# [Patrón de Diseño Creacional/Estructural - Repositorio Singleton]
# Garantiza una única instancia centralizada con diccionarios O(1), tuplas y listas
# ==============================================================================

class RepositorioBiblioteca:
    """
    Repositorio único (Singleton) que indexa publicaciones por ISBN y lectores por código.
    Combina diccionarios (O(1)), tuplas inmutables y listas dinámicas.
    """

    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.catalogo_por_isbn = {}
            cls._instancia.lectores_por_codigo = {}
            cls._instancia.fichas_inmutables = []
            cls._instancia.historial_prestamos = []
        return cls._instancia

    def limpiar_repositorio(self):
        """Reinicia las colecciones internas (útil para pruebas o recargas)."""
        self.catalogo_por_isbn.clear()
        self.lectores_por_codigo.clear()
        self.fichas_inmutables.clear()
        self.historial_prestamos.clear()

    def agregar_publicacion(self, publicacion):
        """Registra una publicación en el diccionario O(1) y guarda su ficha tupla."""
        if publicacion.isbn in self.catalogo_por_isbn:
            raise ValueError(f"Ya existe una publicación registrada con ISBN {publicacion.isbn}.")
        self.catalogo_por_isbn[publicacion.isbn] = publicacion
        self.fichas_inmutables.append(publicacion.obtener_ficha_inmutable())

    def buscar_publicacion_por_isbn(self, isbn):
        """Acceso directo O(1) al diccionario del catálogo."""
        return self.catalogo_por_isbn.get(str(isbn).strip())

    def obtener_lista_catalogo(self):
        """Devuelve una nueva lista (copia superficial) de todas las publicaciones."""
        return list(self.catalogo_por_isbn.values())

    def actualizar_publicacion(self, isbn, datos):
        """Actualiza una publicación conservando su tipo físico o digital."""
        isbn_normalizado = str(isbn).strip()
        actual = self.catalogo_por_isbn.get(isbn_normalizado)
        if actual is None:
            raise KeyError(f"No existe una publicación con ISBN {isbn_normalizado}.")

        tipo = "fisico" if hasattr(actual, "stock") else "ebook"
        datos_actualizados = {
            "isbn": datos.get("isbn", actual.isbn),
            "titulo": datos.get("titulo", actual.titulo),
            "autor": datos.get("autor", actual.autor),
            "genero": datos.get("genero", actual.genero),
            "paginas": datos.get("paginas", actual.paginas),
            "calificacion": datos.get("calificacion", actual.calificacion),
        }
        if tipo == "fisico":
            datos_actualizados["stock"] = datos.get("stock", actual.stock)
            datos_actualizados["ubicacion"] = datos.get("ubicacion", actual.ubicacion)
        else:
            datos_actualizados["formato"] = datos.get("formato", actual.formato)
            datos_actualizados["peso_mb"] = datos.get("peso_mb", actual.peso_mb)

        actualizada = FabricaPublicaciones.crear_publicacion(tipo, **datos_actualizados)
        nuevo_isbn = actualizada.isbn
        if nuevo_isbn != isbn_normalizado and nuevo_isbn in self.catalogo_por_isbn:
            raise ValueError(f"Ya existe una publicación registrada con ISBN {nuevo_isbn}.")

        del self.catalogo_por_isbn[isbn_normalizado]
        self.catalogo_por_isbn[nuevo_isbn] = actualizada
        self.fichas_inmutables = [
            ficha for ficha in self.fichas_inmutables if ficha[0] != isbn_normalizado
        ]
        self.fichas_inmutables.append(actualizada.obtener_ficha_inmutable())
        return actualizada

    def eliminar_publicacion(self, isbn):
        """Elimina una publicación y su ficha inmutable del repositorio."""
        isbn_normalizado = str(isbn).strip()
        eliminada = self.catalogo_por_isbn.pop(isbn_normalizado, None)
        if eliminada is None:
            raise KeyError(f"No existe una publicación con ISBN {isbn_normalizado}.")
        self.fichas_inmutables = [
            ficha for ficha in self.fichas_inmutables if ficha[0] != isbn_normalizado
        ]
        return eliminada

    def agregar_lector(self, lector):
        """Registra un lector indexado por su código único en O(1)."""
        if lector.codigo in self.lectores_por_codigo:
            raise ValueError(f"Ya existe un lector con el código {lector.codigo}.")
        self.lectores_por_codigo[lector.codigo] = lector

    def buscar_lector_por_codigo(self, codigo):
        """Acceso directo O(1) al diccionario de lectores."""
        return self.lectores_por_codigo.get(str(codigo).strip().upper())

    def obtener_lista_lectores(self):
        """Devuelve una nueva lista con los lectores registrados."""
        return list(self.lectores_por_codigo.values())

    def registrar_prestamo(self, registro_prestamo):
        """Agrega un préstamo al historial dinámico."""
        self.historial_prestamos.append(registro_prestamo)
