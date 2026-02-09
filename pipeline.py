from ingestion.loaders import load_pdfs
from ingestion.clean_pdfs import clean_pdfs
from ingestion.chunks_pdfs import chunk_pdfs
from ingestion.embeddings import build_embeddings

RAW_PDFS = "data/raw/pdfs"
PDFS_JSON = "data/processed/pdfs.json"
PDFS_JSON_CLEAN = "data/processed/pdfs_clean.json"
PDFS_CHUNKS = "data/processed/pdfs_chunks.json"
VECTOR_STORE_PATH = "data/vector_store"
COLLECTION_NAME = "pdf_knowledge_base"

def run_pipeline():
    print("🚀 Iniciando pipeline de ingesta\n")

    n_pages = load_pdfs(RAW_PDFS, PDFS_JSON)
    print(f"📄 Páginas cargadas: {n_pages}")

    n_clean = clean_pdfs(PDFS_JSON, PDFS_JSON_CLEAN)
    print(f"🧹 Páginas limpias: {n_clean}")

    n_chunks = chunk_pdfs(PDFS_JSON_CLEAN, PDFS_CHUNKS)
    print(f"🧩 Chunks generados: {n_chunks}")

    n_embeddings = build_embeddings(
        PDFS_CHUNKS,
        VECTOR_STORE_PATH,   
        COLLECTION_NAME
    )
    print(f"Embeddings generados: {n_embeddings}")

    print("\n✅ Pipeline completado correctamente")

if __name__ == "__main__":
    run_pipeline()