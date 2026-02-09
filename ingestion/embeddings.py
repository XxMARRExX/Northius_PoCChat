# ingestion/embeddings.py

import json
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer


def build_embeddings(
    chunks_file: str,
    vector_store_path: str,
    collection_name: str = "pdf_knowledge_base"
) -> int:
    """
    Genera embeddings a partir de chunks y los guarda en un vector store Chroma.
    """

    with open(chunks_file, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    # DEBUG CORRECTO
    # print(type(chunks))
    # print(len(chunks))
    # print(chunks[0].keys())

    # ── cargar chunks ──────────────────────────────
    with open(chunks_file, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    if not chunks:
        return 0

    # ── modelo de embeddings ───────────────────────
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # ── cliente Chroma ─────────────────────────────
    client = chromadb.PersistentClient(
        path=vector_store_path
    )

    collection = client.get_or_create_collection(
        name=collection_name
    )

    # ── preparar datos ─────────────────────────────
    texts = [c["text"] for c in chunks]

    metadatas = [
        {
            "source": c["source"],
            "page": c["page"],
            "chunk_id": c["chunk_id"]
        }
        for c in chunks
    ]

    ids = [str(c["chunk_id"]) for c in chunks]

    # ── generar embeddings ─────────────────────────
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        normalize_embeddings=True
    )
    
    print(type(embeddings))
    print(embeddings.shape)
    print(embeddings[0][:10])

    embeddings = embeddings.tolist()

    # ── insertar en vector store ───────────────────
    collection.add(
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings,
        ids=ids
    )

    return len(chunks)