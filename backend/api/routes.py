import math
import statistics

from fastapi import APIRouter, HTTPException, Query

from backend.models.schemas import (
    RespuestaPublicacion,
    RespuestaRecomendacion,
    SolicitudActualizacionPublicacion,
    SolicitudPublicacion,
)
from backend.services.catalog_service import ServicioCatalogo
from backend.services.recommendation_service import ServicioRecomendaciones
from backend.services.open_library_service import ServicioBibliotecaAbierta


router = APIRouter()
servicio_catalogo = ServicioCatalogo()
servicio_recomendaciones = ServicioRecomendaciones(servicio_catalogo)
biblioteca_abierta = ServicioBibliotecaAbierta()


def crear_respuesta_publicacion(publicacion: object) -> RespuestaPublicacion:
    return RespuestaPublicacion(
        isbn=publicacion.isbn,
        titulo=publicacion.titulo,
        autor=publicacion.autor,
        genero=publicacion.genero,
        paginas=publicacion.paginas,
        calificacion=publicacion.calificacion,
        tipo="fisico" if hasattr(publicacion, "stock") else "ebook",
        formato=getattr(publicacion, "formato", None),
        ubicacion=getattr(publicacion, "ubicacion", None),
        stock=getattr(publicacion, "stock", None),
        peso_mb=getattr(publicacion, "peso_mb", None),
        portada_url=getattr(publicacion, "portada_url", None),
        enlace_abierto=getattr(publicacion, "enlace_abierto", None),
    )


@router.get("/health")
def health():
    return {"estado": "ok"}


@router.get("/publicaciones", response_model=list[RespuestaPublicacion])
def buscar_publicaciones(
    consulta: str = "",
    genero: str = "todos",
    limit: int = Query(default=20, ge=1, le=100),
):
    externas = biblioteca_abierta.buscar(consulta, genero, limit)
    if externas:
        return [
            RespuestaPublicacion(
                isbn=publication["isbn"],
                titulo=publication["title"],
                autor=publication["author"],
                genero=publication["genre"],
                paginas=publication["pages"],
                calificacion=publication["rating"],
                tipo=publication["type"],
                formato=publication["format"],
                portada_url=publication["cover_url"],
                enlace_abierto=publication["open_url"],
                descripcion=publication["description"],
                etiquetas=publication["subjects"],
            )
            for publication in externas
        ]

    publicaciones = servicio_catalogo.buscar(consulta, genero)
    return [crear_respuesta_publicacion(publicacion) for publicacion in publicaciones[:limit]]


@router.get("/publicaciones/{isbn}", response_model=RespuestaPublicacion)
def obtener_publicacion(isbn: str):
    externa = biblioteca_abierta.obtener_publicacion(isbn)
    if externa is not None:
        return RespuestaPublicacion(
            isbn=externa["isbn"],
            titulo=externa["title"],
            autor=externa["author"],
            genero=externa["genre"],
            paginas=externa["pages"],
            calificacion=externa["rating"],
            tipo=externa["type"],
            formato=externa["format"],
            portada_url=externa["cover_url"],
            enlace_abierto=externa["open_url"],
            descripcion=externa["description"],
            etiquetas=externa["subjects"],
        )

    publicacion = servicio_catalogo.obtener_publicacion(isbn)
    if publicacion is None:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")
    return crear_respuesta_publicacion(publicacion)


@router.post("/publicaciones", response_model=RespuestaPublicacion, status_code=201)
def crear_publicacion(solicitud: SolicitudPublicacion):
    try:
        publicacion = servicio_catalogo.crear_publicacion(solicitud.model_dump())
    except (TypeError, ValueError) as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return crear_respuesta_publicacion(publicacion)


@router.put("/publicaciones/{isbn}", response_model=RespuestaPublicacion)
def actualizar_publicacion(isbn: str, solicitud: SolicitudActualizacionPublicacion):
    try:
        publicacion = servicio_catalogo.actualizar_publicacion(
            isbn, solicitud.model_dump(exclude_unset=True)
        )
    except KeyError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except (TypeError, ValueError) as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return crear_respuesta_publicacion(publicacion)


@router.delete("/publicaciones/{isbn}")
def eliminar_publicacion(isbn: str):
    try:
        eliminada = servicio_catalogo.eliminar_publicacion(isbn)
    except KeyError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    return {"eliminada": eliminada.isbn}


@router.get(
    "/recomendaciones/{isbn}",
    response_model=list[RespuestaRecomendacion],
)
def obtener_recomendaciones(
    isbn: str,
    limit: int = Query(default=6, ge=1, le=20),
):
    fuente_externa = biblioteca_abierta.obtener_publicacion(isbn)
    if fuente_externa is not None:
        recomendaciones = biblioteca_abierta.recomendar(isbn, limit)
        return [
            RespuestaRecomendacion(
                publicacion=RespuestaPublicacion(
                    isbn=item["publication"]["isbn"],
                    titulo=item["publication"]["title"],
                    autor=item["publication"]["author"],
                    genero=item["publication"]["genre"],
                    paginas=item["publication"]["pages"],
                    calificacion=item["publication"]["rating"],
                    tipo=item["publication"]["type"],
                    formato=item["publication"]["format"],
                    portada_url=item["publication"]["cover_url"],
                    enlace_abierto=item["publication"]["open_url"],
                    descripcion=item["publication"]["description"],
                    etiquetas=item["publication"]["subjects"],
                ),
                puntaje=item["score"],
                motivos=item["reasons"],
            )
            for item in recomendaciones
        ]

    recomendaciones = servicio_recomendaciones.recomendar(isbn, limit)
    if servicio_catalogo.obtener_publicacion(isbn) is None:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")
    return [
        RespuestaRecomendacion(
            publicacion=crear_respuesta_publicacion(item["publication"]),
            puntaje=item["score"],
            motivos=item["reasons"],
        )
        for item in recomendaciones
    ]


@router.get("/estadisticas")
def obtener_estadisticas():
    publicaciones = servicio_catalogo.listar_publicaciones()
    if not publicaciones:
        return {
            "cantidad": 0,
            "calificacion_promedio": 0,
            "calificacion_mediana": 0,
            "paginas": 0,
            "horas_lectura": 0,
        }

    calificaciones = [publicacion.calificacion for publicacion in publicaciones]
    paginas = sum(publicacion.paginas for publicacion in publicaciones)
    return {
        "cantidad": len(publicaciones),
        "calificacion_promedio": round(statistics.mean(calificaciones), 2),
        "calificacion_mediana": round(statistics.median(calificaciones), 2),
        "paginas": paginas,
        "horas_lectura": math.ceil(paginas / 40),
    }
