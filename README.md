# 🤖 Asistente Virtual PoC (RAG + LLM Local)

Prueba de Concepto (PoC) de un asistente virtual basado en arquitectura **RAG (Retrieval-Augmented Generation)** utilizando:

- LLM local mediante Ollama
- Sentence Transformers para embeddings
- ChromaDB como base de datos vectorial
- Pipeline de ingestión de PDFs y páginas web
- Interfaz conversacional con Streamlit

El sistema permite consultar documentación interna en PDF mediante búsqueda semántica y generación de respuestas contextualizadas.

<img width="789" height="757" alt="image" src="https://github.com/user-attachments/assets/395c38bb-f78e-4ef6-bce1-3f275d1a3634" />

---

## 📌 Objetivo del Proyecto

Construir un asistente capaz de:

- Ingerir documentos PDF y web
- Dividirlos en fragmentos semánticos (chunks)
- Generar embeddings
- Almacenarlos en una base de datos vectorial
- Recuperar contexto relevante
- Generar respuestas usando un modelo LLM local

---

## 🏗️ Arquitectura del Sistema

<img width="5953" height="1719" alt="image" src="https://github.com/user-attachments/assets/934ef1f4-1ede-4087-8636-af417348a314" />

---

## 📂 Estructura del Proyecto

```
NTH-POCCHAT/
│
├── app/                          # Lógica principal del asistente
│   ├── chat_app.py               
│   ├── config_bot.py             
│   ├── intent_classifier.py      
│   └── ollama_client.py         
│
├── ingestion/                    # Pipeline de ingestión y procesamiento
│   ├── load_pdfs.py              
│   ├── clean_pdfs.py             
│   ├── chunks_pdfs.py            
│   ├── create_embeddings.py      
│   │
│   └── web/                      
│       ├── download_web_pages.py 
│       └── clean_raw_web.py      
│
├── data/
│   ├── raw/                      # Datos originales sin procesar
│   │   ├── pdfs/                 
│   │   └── web/                  
│   │
│   └── processed/                # Datos transformados
│       ├── pdfs.json
│       ├── pdfs_chunks.json
│       ├── pdfs_clean_chunks.json
│       ├── web_raw.json
│       └── web_chunks.json
│
├── vector_store/                 # Base de datos vectorial (Chroma persistente)
│
├── pipeline_pdf.py               # Script principal de pipeline para PDFs
├── pipeline_web.py               # Script principal de pipeline para web
├── config.json                   # Configuración general del sistema
└── .gitignore
```

---

### 🔎 Organización por Capas

El proyecto está estructurado en tres capas principales:

1. **Capa de Ingestión**
   - Extracción
   - Limpieza
   - Chunking
   - Embeddings

2. **Capa de Recuperación**
   - Vector store (Chroma)
   - Búsqueda semántica

3. **Capa de Aplicación**
   - Chat
   - Clasificación de intención
   - Construcción de prompts
   - Comunicación con LLM

---

### 🧠 Principio Arquitectónico

Separación clara entre:

- Procesamiento offline (ingestión)
- Recuperación semántica
- Lógica conversacional
- Infraestructura LLM

Esto permite:

- Reprocesar datos sin afectar la app
- Cambiar modelo LLM sin modificar ingestión
- Escalar fuentes (PDF + Web) de forma modular

---

## 🔄 Pipeline de Procesamiento

### 1️⃣ Ingestión de PDFs

- Carga de documentos PDF
- Extracción de texto
- Limpieza básica de formato

---

### 2️⃣ Estrategia de Chunking

Los documentos se dividen en fragmentos para:

- Mejorar la precisión en recuperación
- Optimizar el uso de ventana de contexto del LLM
- Permitir búsqueda semántica eficiente

Parámetros configurables:
- Tamaño del chunk
- Solapamiento entre fragmentos

---

### 3️⃣ Generación de Embeddings

Cada fragmento se transforma en un vector numérico utilizando:

```python
model = SentenceTransformer("all-MiniLM-L6-v2")
```

Estos vectores representan el significado semántico en un espacio de alta dimensión.

---

### 4️⃣ Filtro de Similitud (Eliminación de Duplicados)

Para evitar almacenar contenido redundante, se aplica un filtro basado en similitud coseno:

```python
cosine_similarity(new_embedding, existing_embeddings)
```

Si la similitud ≥ 0.90, el fragmento se considera demasiado similar y no se inserta.

Esto evita:

- Duplicación semántica
- Sesgo en recuperación
- Crecimiento innecesario del vector store

---

### 5️⃣ Base de Datos Vectorial (ChromaDB)

Se almacenan:

- Embeddings
- Texto original
- Metadatos (PDF origen, página, etc.)

El almacenamiento es persistente.

---

### 6️⃣ Fase de Recuperación

Cuando el usuario formula una pregunta:

1. Se genera su embedding.
2. Se buscan los vectores más similares.
3. Se recuperan los Top-K fragmentos más relevantes.

---

### 7️⃣ Generación de Respuesta

Se construye un prompt que incluye:

- Instrucciones del sistema
- Contexto recuperado
- Pregunta del usuario

---

## 👨‍💻 Autor

Cristian Marrero  
Ingeniería Informática  

Prueba de concepto de asistente virtual basado en RAG.

---
