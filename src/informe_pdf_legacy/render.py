import io
import textwrap

import html2text
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import Image

from .canvas import NumberedPageCanvas
from .models import InformePdfData

COVER_SIZE = (595, 840)
FIRMA_SIZE = (200, 150)
FIRMA_ELECTRONICA_POS = (189, 70)
FIRMA_RESIDENTE_X = 80
FIRMA_MEDICO_X = 350
BODY_TEXT_LEADING = 12
FIRST_PAGE_LINE_LIMIT = 30
CONTINUATION_LINE_LIMIT = 41


def render_informe_pdf(data: InformePdfData) -> io.BytesIO:
    """Render a finalized medical report with the legacy ReportLab layout."""
    buffer = io.BytesIO()
    height = A4[1]
    width = A4[0]
    canvas = NumberedPageCanvas(buffer, pagesize=(width, height))

    _draw_cover(canvas, data, width, height)
    canvas.showPage()
    _draw_first_body_page(canvas, data, height)
    canvas.save()
    buffer.seek(0)
    return buffer


def _draw_cover(canvas, data: InformePdfData, width: float, height: float) -> None:
    canvas.setFont("Helvetica-Bold", 22)
    canvas.drawCentredString(width / 2.0, height - 620, data.servicio)

    canvas.setFont("Helvetica", 12)
    canvas.drawCentredString(width / 2.0, height - 655, data.fecha_coloquial)

    Image(data.cover_image_path, *COVER_SIZE).drawOn(canvas, 0, 0)

    canvas.setFont("Helvetica", 18)
    canvas.drawCentredString(width / 2.0, height - 585, data.paciente)


def _draw_first_body_page(canvas, data: InformePdfData, height: float) -> None:
    Image(data.body_image_path, *COVER_SIZE).drawOn(canvas, 0, 0)

    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(28, height - 165, data.identificacion_tipo)
    canvas.setFont("Helvetica", 11)
    canvas.drawString(50, height - 165, data.identificacion_numero)

    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(28, height - 195, "Protocolo Nº: ")
    canvas.setFont("Helvetica", 11)
    canvas.drawString(100, height - 195, data.protocolo)

    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(28, height - 140, "INFORME Nº: ")
    canvas.setFont("Helvetica", 11)
    canvas.drawString(100, height - 140, data.informe_numero)

    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(28, height - 125, "PACIENTE: ")
    canvas.setFont("Helvetica", 11)
    canvas.drawString(90, height - 125, data.paciente)

    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(180, height - 165, "Fecha Nac: ")
    canvas.setFont("Helvetica", 11)
    canvas.drawString(240, height - 165, data.fecha_nacimiento)

    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(390, height - 165, "Sexo: ")
    canvas.setFont("Helvetica", 11)
    canvas.drawString(422, height - 165, data.sexo)

    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(28, height - 180, "Fecha del Estudio: ")
    canvas.setFont("Helvetica", 11)
    canvas.drawString(128, height - 180, data.fecha_estudio)

    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(240, height - 180, "Hora: ")
    canvas.setFont("Helvetica", 11)
    canvas.drawString(270, height - 180, data.hora_estudio)

    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(390, height - 180, "Nº Orden: ")
    canvas.setFont("Helvetica", 11)
    canvas.drawString(445, height - 180, data.nro_orden)

    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(240, height - 195, "Mod. Acceso: ")
    canvas.drawString(390, height - 195, "Fecha Impresión: ")
    canvas.setFont("Helvetica", 11)
    canvas.drawString(315, height - 195, data.modalidad_acceso)
    canvas.drawString(484, height - 195, data.fecha_impresion)

    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(28, height - 235, "Establecimiento: ")
    canvas.setFont("Helvetica", 11)
    canvas.drawString(120, height - 235, data.establecimiento)

    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(28, height - 220, "MÉDICO SOLICITANTE: ")
    canvas.setFont("Helvetica", 11)
    canvas.drawString(158, height - 220, data.medico_solicitante)

    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(28, height - 250, "CÓDIGOS: ")
    canvas.setFont("Helvetica", 11)
    _draw_codigos(canvas, data.codigos, height)

    canvas.line(28, height - 300, 565, height - 300)
    _draw_informe_text(canvas, data, height)


def _draw_codigos(canvas, codigos: list[str], height: float) -> None:
    linejump = 0
    linehorizontal = 0
    line_start = 87
    for codigo in codigos:
        if linejump >= 55:
            linehorizontal += 170
            linejump = 0
        canvas.drawString(line_start + linehorizontal, height - 250 - linejump, codigo)
        linejump += 11


def _html_to_lines(html: str) -> list[str]:
    converter = html2text.HTML2Text()
    converter.body_width = 90
    converter.strong_mark = ""
    converter.emphasis_mark = ""
    converter.unicode_snob = True
    lines = []
    for line in converter.handle(html or "").splitlines():
        if len(line) > 90:
            lines.extend(textwrap.wrap(line, 90))
        else:
            lines.append(line)
    return lines


def _draw_text_block(canvas, text: str, x: float, y: float) -> None:
    writer = canvas.beginText(x, y)
    writer.setLeading(BODY_TEXT_LEADING)
    writer.textLines(text.replace("\\-", "-"))
    canvas.drawText(writer)


def _draw_footer(canvas, data: InformePdfData) -> None:
    canvas.setFont("Helvetica", 8)
    canvas.drawString(*FIRMA_ELECTRONICA_POS, data.footer_text)


def _draw_mid_page_signature(canvas, data: InformePdfData) -> None:
    canvas.setFont("Helvetica-Bold", 10)
    _draw_signature_text(canvas, data, 90)
    _draw_footer(canvas, data)


def _draw_signature_image(canvas, image_path: str | None, x: float, y: float) -> None:
    if not image_path:
        return
    try:
        Image(image_path, *FIRMA_SIZE).drawOn(canvas, x, y)
    except Exception:
        pass


def _draw_signature_text(canvas, data: InformePdfData, specialty_y: float) -> None:
    if data.firma_residente_nombre:
        canvas.drawString(FIRMA_RESIDENTE_X, specialty_y + 10, data.firma_residente_nombre)
        canvas.drawString(FIRMA_RESIDENTE_X, specialty_y, data.firma_residente_especialidad)
    canvas.drawString(FIRMA_MEDICO_X, specialty_y + 10, data.firma_nombre)
    canvas.drawString(FIRMA_MEDICO_X, specialty_y, data.firma_especialidad)


def _draw_signature_images(canvas, data: InformePdfData, y: float) -> None:
    if data.firma_residente_nombre:
        _draw_signature_image(canvas, data.firma_residente_image_path, FIRMA_RESIDENTE_X, y)
    _draw_signature_image(canvas, data.firma_image_path, FIRMA_MEDICO_X, y)


def _draw_continuation_header(canvas, data: InformePdfData) -> None:
    Image(data.body_image_path, *COVER_SIZE).drawOn(canvas, 0, 0)
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(28, A4[1] - 128, "INFORME Nº: " + data.informe_numero)
    canvas.drawString(28, A4[1] - 145, "Fecha del Estudio: " + data.fecha_estudio_continuacion)
    canvas.drawString(250, A4[1] - 145, "Hora: " + data.hora_estudio_continuacion)
    canvas.drawString(450, A4[1] - 162, data.documento)
    canvas.drawString(28, A4[1] - 162, "Paciente: " + data.paciente)
    canvas.line(25, A4[1] - 115, 565, A4[1] - 115)
    canvas.line(25, A4[1] - 165, 565, A4[1] - 165)
    canvas.line(25, A4[1] - 115, 25, A4[1] - 165)
    canvas.line(565, A4[1] - 115, 565, A4[1] - 165)


def _draw_informe_text(canvas, data: InformePdfData, height: float) -> None:
    lines = _html_to_lines(data.contenido_html)
    if len(lines) > FIRST_PAGE_LINE_LIMIT:
        _draw_multipage_text(canvas, data, height, lines)
        return
    _draw_single_page_text(canvas, data, lines)


def _draw_single_page_text(canvas, data: InformePdfData, lines: list[str]) -> None:
    text = "".join("\n" + line for line in lines)
    canvas.setFont("Helvetica", 11)
    _draw_text_block(canvas, text, 28, 525)
    canvas.setFont("Helvetica-Bold", 10)
    line_final = max(375 - len(lines) * BODY_TEXT_LEADING, 73)
    _draw_signature_images(canvas, data, line_final)
    _draw_signature_text(canvas, data, line_final + 5)
    _draw_footer(canvas, data)
    canvas.showPage()


def _draw_multipage_text(
    canvas,
    data: InformePdfData,
    height: float,
    lines: list[str],
) -> None:
    first_page = "".join("\n" + line for line in lines[:FIRST_PAGE_LINE_LIMIT])
    canvas.setFont("Helvetica", 11)
    _draw_text_block(canvas, first_page, 28, 525)
    _draw_mid_page_signature(canvas, data)
    canvas.showPage()

    chunk = ""
    linecount = 0
    for line in lines[FIRST_PAGE_LINE_LIMIT:]:
        linecount += 1
        chunk += "\n" + line
        if linecount % CONTINUATION_LINE_LIMIT == 0:
            _draw_continuation_header(canvas, data)
            canvas.setFont("Helvetica", 11)
            _draw_text_block(canvas, chunk, 28, A4[1] - 190)
            _draw_mid_page_signature(canvas, data)
            canvas.showPage()
            chunk = ""

    resto = (len(lines) - FIRST_PAGE_LINE_LIMIT) % CONTINUATION_LINE_LIMIT
    start = len(lines) - resto
    last_page = "".join("\n" + lines[start + i] for i in range(resto))
    _draw_continuation_header(canvas, data)
    canvas.setFont("Helvetica", 11)
    _draw_text_block(canvas, last_page, 28, A4[1] - 190)
    canvas.setFont("Helvetica-Bold", 10)
    line_final = max(height - 12 * cm - resto * BODY_TEXT_LEADING, 73)
    _draw_signature_images(canvas, data, line_final)
    _draw_signature_text(canvas, data, line_final - 12)
    _draw_footer(canvas, data)
    canvas.showPage()
