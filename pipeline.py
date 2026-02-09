from ingestion.loaders import load_pdfs
from ingestion.clean_pdfs import clean_pdfs

RAW_PDFS = "data/raw/pdfs"
PDFS_JSON = "data/processed/pdfs.json"
PDFS_JSON_CLEAN = "data/processed/pdfs_clean.json"

def run_pipeline():
    print("🚀 Iniciando pipeline de ingesta\n")

    n_pages = load_pdfs(RAW_PDFS, PDFS_JSON)
    print(f"📄 Páginas cargadas: {n_pages}")

    n_clean = clean_pdfs(PDFS_JSON, PDFS_JSON_CLEAN)
    print(f"🧹 Páginas limpias: {n_clean}")

    print("\n✅ Pipeline completado correctamente")

if __name__ == "__main__":
    run_pipeline()