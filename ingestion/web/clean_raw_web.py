import json
import os
import time
import re
from typing import List, Dict
from bs4 import BeautifulSoup

def extract_titles_and_paragraphs(html: str) -> str:
    """
    Extrae SOLO:
    - h1, h2, h3, h4, h5, h6
    - p

    Devuelve texto normalizado y ordenado tal como aparece en el HTML.
    """

    soup = BeautifulSoup(html, "html.parser")

    parts: List[str] = []

    # Recorremos el DOM en orden de aparición
    for tag in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p"]):
        text = tag.get_text(" ", strip=True)
        if not text:
            continue

        if tag.name.startswith("h"):
            level = int(tag.name[1])
            parts.append("\n" + "#" * level + " " + text + "\n")
        else:  # párrafo
            parts.append(text)

    # Normalización básica de espacios
    clean_text = "\n".join(parts)
    clean_text = "\n".join([line.strip() for line in clean_text.splitlines() if line.strip()])

    return clean_text



def clean_web(raw_index_json: str, output_json: str) -> int:
    """
    - Lee el índice de páginas descargadas (raw_index_json)
    - Carga cada HTML desde data/raw/web/
    - Extrae SOLO títulos y párrafos
    - Genera web_clean.json (formato compatible con chunk_pdfs)
    """

    with open(raw_index_json, "r", encoding="utf-8") as f:
        pages: List[Dict] = json.load(f)

    cleaned_pages = []
    count = 0

    for page in pages:
        url = page["url"]
        filename = page["filename"]
        html_path = os.path.join("data/raw/web", filename)

        if not os.path.exists(html_path):
            print(f"⚠️ HTML no encontrado para {url} → {filename}")
            continue

        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()

        clean_text = extract_titles_and_paragraphs(html)

        cleaned_pages.append({
            "source": filename,   # <-- equivalente a PDFs
            "page": "web",        # <-- equivalente a número de página
            "text": clean_text,   # <-- lo que luego se va a chunkear
            "url": url            # <-- tu requisito (se conserva)
        })

        count += 1

    os.makedirs(os.path.dirname(output_json), exist_ok=True)
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(cleaned_pages, f, ensure_ascii=False, indent=2)

    return count

