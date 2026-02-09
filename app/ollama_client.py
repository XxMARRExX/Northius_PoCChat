# app/ollama_client.py
import ollama

def llamar_a_ollama(prompt, model="llama3:8b"):
    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": "Eres un asistente útil."},
            {"role": "user", "content": prompt}
        ]
    )
    return response["message"]["content"]
