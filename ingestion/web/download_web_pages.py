import json
import os
import time
import requests

def _url_to_filename(url: str) -> str:
    name = url.replace("https://", "").replace("http://", "").replace("/", "_")
    return f"{name}.html"

def download_web_pages(input_urls_json: str, raw_web_dir: str, index_json: str) -> int:
    """
    Descarga cada URL a data/raw/web/*.html y VA RELLENANDO un JSON índice
    con {url, filename, downloaded_at}.
    """

    os.makedirs(raw_web_dir, exist_ok=True)

    # Leer lista de URLs
    with open(input_urls_json, "r", encoding="utf-8") as f:
        urls = json.load(f)

    # Si el índice ya existe, lo cargamos para ir ampliándolo
    if os.path.exists(index_json):
        with open(index_json, "r", encoding="utf-8") as f:
            index = json.load(f)
    else:
        index = []

    existing_urls = {item["url"] for item in index}

    count = 0

    for url in urls:
        if url in existing_urls:
            print(f"ℹ️ Ya descargada (se omite): {url}")
            continue

        print(f"🌐 Descargando: {url}")

        try:
            r = requests.get(url, timeout=20)
            r.raise_for_status()

            filename = _url_to_filename(url)
            filepath = os.path.join(raw_web_dir, filename)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(r.text)

            record = {
                "url": url,
                "filename": filename,
                "downloaded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }

            index.append(record)
            count += 1

        except Exception as e:
            print(f"⚠️ Error descargando {url}: {e}")

    # Guardar (o actualizar) el índice JSON
    with open(index_json, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    return count
