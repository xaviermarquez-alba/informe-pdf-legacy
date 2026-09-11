from dataclasses import dataclass, field


DEFAULT_FOOTER = (
    "El presente informe medico a sido firmado por el profesional "
    "responsable mediante firma electrónica."
)
DEFAULT_ESPECIALIDAD = "Esp. Diagnóstico por Imágenes"
DEFAULT_RESIDENTE_ESPECIALIDAD = "Medico"


@dataclass
class InformePdfData:
    """Display-ready fields for the legacy ReportLab informe layout.

    Dates, timezone conversion, patient identity, service labels and
    finalized snapshots belong to the calling application.
    """

    paciente: str
    servicio: str
    fecha_coloquial: str
    informe_numero: str
    identificacion_tipo: str
    identificacion_numero: str
    documento: str
    protocolo: str
    fecha_nacimiento: str
    sexo: str
    fecha_estudio: str
    hora_estudio: str
    fecha_estudio_continuacion: str
    hora_estudio_continuacion: str
    nro_orden: str
    modalidad_acceso: str
    fecha_impresion: str
    establecimiento: str
    medico_solicitante: str
    contenido_html: str
    firma_nombre: str
    cover_image_path: str
    body_image_path: str
    codigos: list[str] = field(default_factory=list)
    firma_image_path: str | None = None
    firma_especialidad: str = DEFAULT_ESPECIALIDAD
    footer_text: str = DEFAULT_FOOTER
    firma_residente_nombre: str | None = None
    firma_residente_image_path: str | None = None
    firma_residente_especialidad: str = DEFAULT_RESIDENTE_ESPECIALIDAD
