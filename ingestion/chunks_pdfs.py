# ingestion/chunk_pdfs.py
import json
from pathlib import Path

def chunk_text(text, size, overlap):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start+size])
        start += size - overlap
    return chunks

def chunk_pdfs(input_file: str, output_file: str,
               chunk_size=800, overlap=160):

    with open(input_file, "r", encoding="utf-8") as f:
        pages = json.load(f)

    chunks_out = []

    for r in pages:
        chunks = chunk_text(r["text"], chunk_size, overlap)
        for i, chunk in enumerate(chunks):
            chunks_out.append({
                "source": r["source"],
                "page": r["page"],
                "chunk_index": i + 1,
                "chunk_id": f"{r['source']}_p{r['page']}_c{i+1}",
                "text": chunk
            })

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(chunks_out, f, ensure_ascii=False, indent=2)

    return len(chunks_out)
