import json
from ingestion.load_pdfs import load_pdfs
from ingestion.clean_pdfs import clean_pdfs
from ingestion.chunks_pdfs import chunk_pdfs
from ingestion.create_embeddings import build_embeddings

# --- Rutas ---
RAW_PDFS = "data/raw/pdfs"
PDFS_JSON = "data/processed/pdfs.json"
PDFS_JSON_CLEAN = "data/processed/pdfs_clean_chunks.json"
PDFS_CHUNKS = "data/processed/pdfs_chunks.json"
VECTOR_STORE_PATH = "data/vector_store"
COLLECTION_NAME = "pdf_knowledge_base"

CONFIG_PATH = "config.json"

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def run_pipeline():
    print("🚀 Iniciando pipeline de ingesta\n")

    config = load_config()

    if not config["pdf_pipeline"]["pdf_load_done"]:
        n_pages = load_pdfs(RAW_PDFS, PDFS_JSON)
        print(f"📄 Páginas cargadas: {n_pages}")
        config["pdf_load_done"] = True
        save_config(config)
    else:
        print("ℹ️ Carga de PDFs ya realizada → se omite")

    if not config["pdf_pipeline"]["pdf_clean_done"]:
        n_clean = clean_pdfs(PDFS_JSON, PDFS_JSON_CLEAN)
        print(f"🧹 Páginas limpias: {n_clean}")
        config["pdf_clean_done"] = True
        save_config(config)
    else:
        print("ℹ️ Limpieza ya realizada → se omite")

    if not config["pdf_pipeline"]["pdf_chunk_done"]:
        n_chunks = chunk_pdfs(PDFS_JSON_CLEAN, PDFS_CHUNKS)
        print(f"🧩 Chunks generados: {n_chunks}")
        config["pdf_chunk_done"] = True
        save_config(config)
    else:
        print("ℹ️ Chunking ya realizado → se omite")


    if not config["pdf_pipeline"]["pdf_embeddings_done"]:
        n_embeddings = build_embeddings(
            PDFS_CHUNKS,
            VECTOR_STORE_PATH,
            COLLECTION_NAME
        )
        print(f"Embeddings generados: {n_embeddings}")
        config["pdf_embeddings_done"] = True
        save_config(config)
    else:
        print("ℹ️ Embeddings ya generados → se omite")

    print("\n✅ Pipeline completado correctamente")

if __name__ == "__main__":
    run_pipeline()
