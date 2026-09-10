# informe-pdf-legacy

Python library extracted from TCSE's ReportLab `informe_medico_generar_pdf`.
It renders finalized medical reports to PDF using the original canvas layout:
cover page, first-page header, continuation headers, signature image and footer.

It does not depend on Django, a database, patient models or application credentials.
Dates, timezone conversion, patient identity, service labels and immutable
finalized snapshots belong to the calling application.

This is the ReportLab implementation. The HTML/Chromium renderer lives in
[informe-pdf](https://github.com/xaviermarquez-alba/informe-pdf) and is a
separate Node.js package. The two engines are not layout-compatible.

## Requirements

Python 3.11+.

## Development and installation

```sh
python -m pip install -e ".[dev]"
pytest
```

Install directly from the private GitHub repository using an authenticated SSH connection:

```sh
pip install git+ssh://git@github.com/xaviermarquez-alba/informe-pdf-legacy.git
```

Pin a commit or tag for reproducible installations.

## Direct usage

```python
from informe_pdf_legacy import InformePdfData, render_informe_pdf

data = InformePdfData(
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
    contenido_html="<p>Hallazgos de ejemplo.</p>",
    firma_nombre="Dr. Informante, Ejemplo - MP 123",
    cover_image_path="/absolute/path/to/imageninforme1.png",
    body_image_path="/absolute/path/to/imageninforme2.png",
    codigos=["CT01 - Estudio"],
    # firma_image_path="/absolute/path/to/firma.png",
)
buffer = render_informe_pdf(data)
# buffer is a BytesIO of PDF bytes
```

`InformePdfData` describes display-ready fields. Branding images are supplied
by callers. This is visual signature rendering, not cryptographic PDF signing.

Application permissions, finalization, file storage and database transactions
remain in Django. Existing stored PDFs should still be served without rendering again.
