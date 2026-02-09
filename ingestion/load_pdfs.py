# ingestion/load_pdfs.py
import os
import json
from pypdf import PdfReader
from pathlib import Path

def load_pdfs(input_folder: str, output_file: str):
    records = []

    for filename in os.listdir(input_folder):
        if not filename.lower().endswith(".pdf"):
            continue

        path = os.path.join(input_folder, filename)
        reader = PdfReader(path)
        total_pages = len(reader.pages)

        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            if text and text.strip():
                records.append({
                    "source": filename,
                    "page": f"{page_num + 1}/{total_pages}",
                    "text": text
                })

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    return len(records)
