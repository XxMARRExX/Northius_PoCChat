import json
import chromadb
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------------------
# Funciones de deduplicación
# ---------------------------

def is_too_similar(new_emb: np.ndarray,
                   existing_embs: list[np.ndarray],
                   threshold: float = 0.90) -> bool:
    if not existing_embs:
        return False

    sims = cosine_similarity([new_emb], existing_embs)[0]
    return float(np.max(sims)) >= threshold


def deduplicate_chunks_semantic(chunks, embedder, threshold: float = 0.90):
    kept_chunks = []
    kept_embeddings = []

    for chunk in chunks:
        emb = embedder.encode(
            chunk["text"],
            normalize_embeddings=True
        )

        if not is_too_similar(emb, kept_embeddings, threshold):
            kept_chunks.append(chunk)
            kept_embeddings.append(emb)

    return kept_chunks, kept_embeddings



def build_embeddings(
    chunks_file: str,
    vector_store_path: str,
    collection_name: str
) -> int:

    # 1) Cargar chunks (PDF o Web, da igual)
    with open(chunks_file, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    if not chunks:
        return 0

    # 2) Cargar modelo
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # 3) Cliente Chroma
    client = chromadb.PersistentClient(path=vector_store_path)
    collection = client.get_or_create_collection(name=collection_name)

    print(f"🔹 Chunks antes de deduplicar: {len(chunks)}")

    # 4) DEDUPLICACIÓN SEMÁNTICA (AQUÍ OCURRE TODO)
    filtered_chunks, filtered_embeddings = deduplicate_chunks_semantic(
        chunks,
        model,
        threshold=0.90
    )

    print(f"🔹 Chunks después de deduplicar: {len(filtered_chunks)}")

    # 5) Preparar datos finales para Chroma
    texts = [c["text"] for c in filtered_chunks]

    metadatas = []
    ids = []

    for c in filtered_chunks:
        meta = {
            "source": c["source"],
            "page": c["page"],
            "chunk_id": c["chunk_id"]
        }

        # 🔹 IMPORTANTE: solo para WEB conservamos la URL
        if "url" in c:
            meta["url"] = c["url"]

        metadatas.append(meta)
        ids.append(str(c["chunk_id"]))

    embeddings = [e.tolist() for e in filtered_embeddings]

    # 6) Guardar en Chroma
    collection.add(
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings,
        ids=ids
    )

    return len(filtered_chunks)
