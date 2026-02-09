from ingestion.loaders import load_pdfs

RAW_PDFS = "data/raw/pdfs"
PDFS_JSON = "data/processed/pdfs.json"

def run_pipeline():
    print("🚀 Iniciando pipeline de ingesta\n")

    n_pages = load_pdfs(RAW_PDFS, PDFS_JSON)
    print(f"📄 Páginas cargadas: {n_pages}")

    

    print("\n✅ Pipeline completado correctamente")

if __name__ == "__main__":
    run_pipeline()