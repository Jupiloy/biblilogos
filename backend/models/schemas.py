from pydantic import BaseModel, Field


class RespuestaPublicacion(BaseModel):
    isbn: str
    titulo: str
    autor: str
    genero: str
    paginas: int
    calificacion: float
    tipo: str
    formato: str | None = None
    ubicacion: str | None = None
    stock: int | None = None
    peso_mb: float | None = None
    portada_url: str | None = None
    enlace_abierto: str | None = None
    descripcion: str | None = None
    etiquetas: list[str] = Field(default_factory=list)


class RespuestaRecomendacion(BaseModel):
    publicacion: RespuestaPublicacion
    puntaje: float
    motivos: list[str]
