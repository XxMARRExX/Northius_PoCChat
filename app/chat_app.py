import streamlit as st
import chromadb
from sentence_transformers import SentenceTransformer
import ollama
from intent_classifier import clasificar_intencion
from config_bot import BOT_RULES

# ── Config ──────────────────────────────────────
VECTOR_STORE_PATH = "data/vector_store"
COLLECTION_NAME = "pdf_knowledge_base"
TOP_K = 5

# ── Cargar modelos una sola vez ─────────────────
@st.cache_resource
def load_models():
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path=VECTOR_STORE_PATH)
    collection = client.get_collection(name=COLLECTION_NAME)
    return embedder, collection

embedder, collection = load_models()

# ── UI ──────────────────────────────────────────
st.set_page_config(page_title="Chat Nubika", page_icon="🤖")
st.title("🤖 Asistente Nubika (PoC)")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input del usuario
if question := st.chat_input("Escribe tu pregunta..."):

    # Guardar mensaje usuario
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )
    with st.chat_message("user"):
        st.markdown(question)

    intencion = clasificar_intencion(question)

    # ── RAG ──────────────────────────────────────
    query_embedding = embedder.encode(
        question,
        normalize_embeddings=True
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=TOP_K
    )

    chunks = results["documents"][0]

    context = "\n\n".join(
        f"- {chunk}" for chunk in chunks
    )

    prompt = f"""
Eres un asistente comercial de Nubika.

REGLAS OBLIGATORIAS:
{chr(10).join(BOT_RULES["mandatory_behaviors"])}

PROHIBICIONES:
{chr(10).join(BOT_RULES["prohibitions"])}

OBJETIVOS DE NEGOCIO:
{chr(10).join(BOT_RULES["business_objectives"])}

ESTILO Y SEGURIDAD:
- Nunca seas hiriente, sarcástico o conflictivo.
- Responde siempre en español.
- Si no sabes algo con certeza, dilo claramente.

TIPO DE INTERACCIÓN DETECTADO: {intencion}

CONTEXTO (usa SOLO esto para hablar de Nubika):
{context}

PREGUNTA DEL USUARIO:
{question}

INSTRUCCIONES FINALES:
- Si te piden precios, NO los des y redirige a una llamada.
- Intenta siempre, de forma natural, avanzar hacia agendar una llamada.
"""

    # ── LLaMA local ─────────────────────────────
    response = ollama.chat(
        model="llama3:8b",
        messages=[
            {"role": "system", "content": "Eres un asistente informativo y preciso."},
            {"role": "user", "content": prompt}
        ]
    )

    answer = response["message"]["content"]

    # Guardar respuesta
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    with st.chat_message("assistant"):
        st.markdown(answer)

