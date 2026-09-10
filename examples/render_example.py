"""Minimal example. Replace image paths before running."""
from pathlib import Path

from informe_pdf_legacy import InformePdfData, render_informe_pdf

HERE = Path(__file__).resolve().parent


def main() -> None:
    data = InformePdfData(
        paciente="PACIENTE, EJEMPLO",
        servicio="TOMOGRAFÍA COMPUTADA",
        fecha_coloquial="10 de Septiembre del 2026",
        informe_numero="IN000001",
        identificacion_tipo="DNI: ",
        identificacion_numero="EJEMPLO",
        documento="DNI: EJEMPLO",
        protocolo="CT0001",
        fecha_nacimiento="01-01-1980",
        sexo="M",
        fecha_estudio="10-09-2026",
        hora_estudio="10:30",
        fecha_estudio_continuacion="10-09-2026",
        hora_estudio_continuacion="10:30",
        nro_orden="1-R",
        modalidad_acceso="Ambulatorio",
        fecha_impresion="10-09-26 11:00",
        establecimiento="Establecimiento de ejemplo",
        medico_solicitante="Dr. Ejemplo",
        contenido_html="<p>Contenido de demostración, sin datos reales.</p>",
        firma_nombre="Dra. Ejemplo - MP 123",
        cover_image_path=str(HERE / "imageninforme1.png"),
        body_image_path=str(HERE / "imageninforme2.png"),
        codigos=["CT01 - Estudio de ejemplo"],
    )
    output = HERE / "informe-ejemplo.pdf"
    output.write_bytes(render_informe_pdf(data).getvalue())
    print(output)


if __name__ == "__main__":
    main()
