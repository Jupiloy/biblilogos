from pydantic import BaseModel, Field, model_validator


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


class SolicitudPublicacion(BaseModel):
    isbn: str
    titulo: str
    autor: str
    genero: str
    paginas: int = Field(gt=0)
    calificacion: float = Field(ge=0.0, le=5.0)
    tipo: str = Field(pattern="^(fisico|ebook)$")
    stock: int | None = Field(default=None, ge=0)
    ubicacion: str | None = None
    formato: str | None = None
    peso_mb: float | None = Field(default=None, gt=0)

    @model_validator(mode="after")
    def validar_datos_especificos(self):
        if self.tipo == "fisico" and (
            self.stock is None or not self.ubicacion or not self.ubicacion.strip()
        ):
            raise ValueError(
                "Las publicaciones físicas requieren stock y ubicación."
            )
        if self.tipo == "ebook" and (
            self.formato is None or self.peso_mb is None
        ):
            raise ValueError("Los ebooks requieren formato y peso en MB.")
        return self


class SolicitudActualizacionPublicacion(BaseModel):
    isbn: str | None = None
    titulo: str | None = None
    autor: str | None = None
    genero: str | None = None
    paginas: int | None = Field(default=None, gt=0)
    calificacion: float | None = Field(default=None, ge=0.0, le=5.0)
    stock: int | None = Field(default=None, ge=0)
    ubicacion: str | None = None
    formato: str | None = None
    peso_mb: float | None = Field(default=None, gt=0)
