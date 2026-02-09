import json
import re
from collections import Counter
from pathlib import Path

# ─────────────────────────────────────────────
# Filtros (internos al módulo)
# ─────────────────────────────────────────────
def filter_editorial_lines(text: str) -> str:
    banned_keywords = [
        "CTA",
        "Comentado",
        "Miniatura",
        "FORMULARIO",
        "pop up",
        "Ver más",
        "Solicitar información",
        "sharepoint",
        "ESPACIO PARA",
        "@"
    ]

    cleaned_lines = []

    for line in text.splitlines():
        line_stripped = line.strip()
        if not line_stripped:
            continue

        if any(k.lower() in line_stripped.lower() for k in banned_keywords):
            continue

        cleaned_lines.append(line_stripped)

    return "\n".join(cleaned_lines)



def filter_emojis_and_placeholders(text: str) -> str:
    text = re.sub(r"\[EMOJI.*?\]", "", text, flags=re.IGNORECASE)

    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F700-\U0001F77F"
        "\U0001F780-\U0001F7FF"
        "\U0001F800-\U0001F8FF"
        "\U0001F900-\U0001F9FF"
        "\U0001FA00-\U0001FAFF"
        "]+",
        flags=re.UNICODE
    )

    return emoji_pattern.sub("", text)



def split_semantic_blocks(text: str) -> list[str]:
    separators = ["-----", "\n\n"]
    blocks = [text]

    for sep in separators:
        new_blocks = []
        for block in blocks:
            parts = block.split(sep)
            new_blocks.extend(p.strip() for p in parts if p.strip())
        blocks = new_blocks

    return blocks



def filter_ui_artifacts(text: str) -> str:
    banned = [
        "LOGO", "IMG", "VÍDEO", "widget", "POP-UP",
        "Footer", "H1", "H2", "Cards", "icono"
    ]
    return "\n".join(
        line for line in text.splitlines()
        if not any(b.lower() in line.lower() for b in banned)
    )



def filter_editorial_future_notes(text: str) -> str:
    banned = [
        "aún no existe",
        "prevemos",
        "maquetamos",
        "de momento",
        "en diseño",
        "no se activa"
    ]
    return "\n".join(
        line for line in text.splitlines()
        if not any(b in line.lower() for b in banned)
    )




# ─────────────────────────────────────────────
# FUNCIÓN PÚBLICA (la que llama el pipeline)
# ─────────────────────────────────────────────
def clean_pdfs(input_file: str, output_file: str) -> int:
    """
    Limpia el texto de los PDFs:
    - elimina cabeceras/pies repetidos
    - elimina líneas editoriales
    - elimina emojis y placeholders
    - elimina artefactos de UI
    - elimina notas editoriales futuras
    - elimina marketing emocional corto
    - normaliza espacios
    """

    with open(input_file, "r", encoding="utf-8") as f:
        pages = json.load(f)

    # 1️⃣ detectar cabeceras/pies repetidos por PDF
    lines_per_pdf = {}

    for r in pages:
        pdf = r["source"]
        lines = [l.strip() for l in r["text"].splitlines() if l.strip()]
        lines_per_pdf.setdefault(pdf, []).extend(lines[:2] + lines[-2:])

    common_lines = {}
    for pdf, lines in lines_per_pdf.items():
        counter = Counter(lines)
        threshold = 0.6 * len([r for r in pages if r["source"] == pdf])
        common_lines[pdf] = {
            l for l, c in counter.items() if c >= threshold
        }

    # 2️⃣ limpieza real (subetapa)
    cleaned = []

    for r in pages:
        text = r["text"]

        # ── eliminar cabeceras/pies ─────────────────────
        text = "\n".join(
            l for l in text.splitlines()
            if l.strip() and l.strip() not in common_lines.get(r["source"], set())
        )

        # ── filtros semánticos (orden IMPORTANTE) ───────
        text = filter_editorial_lines(text)
        text = filter_emojis_and_placeholders(text)
        text = filter_ui_artifacts(text)
        text = filter_editorial_future_notes(text)

        # ── normalización final ─────────────────────────
        text = re.sub(r"\s+", " ", text).strip()

        if text:
            cleaned.append({**r, "text": text})

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)

    return len(cleaned)

