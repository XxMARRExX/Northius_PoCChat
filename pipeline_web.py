import json
from ingestion.web.download_web_pages import download_web_pages
from ingestion.web.clean_raw_web import clean_web
from ingestion.chunks_pdfs import chunk_pdfs
from ingestion.create_embeddings import build_embeddings

# --- Rutas ---
WEB_PAGES = "data/raw/web/pages.json"
WEB_RAW_DIR = "data/raw/web"
WEB_INDEX = "data/raw/web/index.json"
WEB_RAW = "data/processed/web_raw.json"
WEB_CHUNKS = "data/processed/web_chunks.json"

VECTOR_STORE_PATH = "data/vector_store"
COLLECTION_NAME = "web_knowledge_base"

CONFIG_PATH = "config.json"

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def run_pipeline_web():
    print("🌐🚀 Iniciando pipeline de ingesta WEB\n")

    config = load_config()

    # ---------------------------
    # 1) DESCARGA DE HTML
    # ---------------------------
    if not config["web_pipeline"]["web_download_done"]:
        n_downloaded = download_web_pages(
            WEB_PAGES,
            WEB_RAW_DIR,
            WEB_INDEX
        )
        print(f"📥 Páginas HTML descargadas: {n_downloaded}")

        config["web_pipeline"]["web_download_done"] = True
        save_config(config)
    else:
        print("ℹ️ Descarga web ya realizada → se omite")

    # ---------------------------
    # 2) LIMPIEZA WEB
    # ---------------------------
    if not config["web_pipeline"]["web_clean_done"]:
        n_web_clean = clean_web(
            WEB_INDEX,
            WEB_RAW
        )
        print(f"🧹 Páginas web limpias: {n_web_clean}")

        config["web_pipeline"]["web_clean_done"] = True
        save_config(config)
    else:
        print("ℹ️ Limpieza web ya realizada → se omite")

    # ---------------------------
    # 3) CHUNKING WEB
    # ---------------------------
    if not config["web_pipeline"]["web_chunk_done"]:
        n_web_chunks = chunk_pdfs(
            WEB_RAW,
            WEB_CHUNKS,
            chunk_size=800,
            overlap=160
        )
        print(f"🧩 Chunks generados (Web): {n_web_chunks}")

        config["web_pipeline"]["web_chunk_done"] = True
        save_config(config)
    else:
        print("ℹ️ Chunking web ya realizado → se omite")

    # ---------------------------
    # 4) EMBEDDINGS WEB
    # ---------------------------
    if not config["web_pipeline"]["web_embeddings_done"]:
        n_embeddings = build_embeddings(
            WEB_CHUNKS,
            VECTOR_STORE_PATH,
            COLLECTION_NAME
        )
        print(f"🔢 Embeddings finales almacenados: {n_embeddings}")

        config["web_pipeline"]["web_embeddings_done"] = True
        save_config(config)
    else:
        print("ℹ️ Embeddings web ya generados → se omite")

    print("\n✅ Pipeline WEB completado correctamente")

if __name__ == "__main__":
    run_pipeline_web()
