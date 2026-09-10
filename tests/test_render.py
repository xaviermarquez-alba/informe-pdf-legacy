from pathlib import Path

from PIL import Image as PILImage

from informe_pdf_legacy import InformePdfData, render_informe_pdf


def _png(path: Path, size=(8, 8), color=(240, 240, 240)) -> str:
    image = PILImage.new("RGB", size, color)
    image.save(path)
    return str(path)


def _sample(tmp_path: Path, html: str, **overrides) -> InformePdfData:
    values = dict(
        paciente="PACIENTE, EJEMPLO",
        servicio="TOMOGRAFÍA COMPUTADA",
        fecha_coloquial="10 de Septiembre del 2026",
        informe_numero="IN000001",
        identificacion_tipo="DNI: ",
        identificacion_numero="12345678",
        documento="DNI: 12345678",
        protocolo="CT0001",
        fecha_nacimiento="01-01-1980",
        sexo="M",
        fecha_estudio="10-09-2026",
        hora_estudio="10:30",
        fecha_estudio_continuacion="10-09-2026",
        hora_estudio_continuacion="10:30",
        nro_orden="123-R",
        modalidad_acceso="Ambulatorio",
        fecha_impresion="10-09-26 11:00",
        establecimiento="Hospital de ejemplo",
        medico_solicitante="Dr. Ejemplo",
        contenido_html=html,
        firma_nombre="Dr. Informante, Ejemplo - MP 123",
        cover_image_path=_png(tmp_path / "cover.png", color=(220, 220, 255)),
        body_image_path=_png(tmp_path / "body.png", color=(255, 255, 255)),
        firma_image_path=_png(tmp_path / "firma.png", size=(40, 20), color=(10, 10, 10)),
        codigos=["CT01 - Estudio de ejemplo"],
    )
    values.update(overrides)
    return InformePdfData(**values)


def test_render_returns_pdf_bytes(tmp_path):
    buffer = render_informe_pdf(_sample(tmp_path, "<p>Hallazgo de ejemplo.</p>"))
    payload = buffer.getvalue()
    assert payload.startswith(b"%PDF")
    assert len(payload) > 1000


def test_long_content_produces_continuation_pages(tmp_path):
    paragraphs = "".join(f"<p>Linea de informe numero {i:03d} con texto de relleno.</p>" for i in range(80))
    buffer = render_informe_pdf(_sample(tmp_path, paragraphs))
    payload = buffer.getvalue()
    assert payload.startswith(b"%PDF")
    page_count = payload.count(b"/Type /Page") + payload.count(b"/Type/Page")
    assert page_count >= 3
