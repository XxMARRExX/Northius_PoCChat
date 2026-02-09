from ollama_client import llamar_a_ollama

def clasificar_intencion(mensaje: str) -> str:
    prompt = f"""
    Clasifica la intención del usuario en UNA de estas categorías:
    - INFORMACIÓN_GENERAL
    - PREGUNTA_CURSO
    - OBJECIÓN
    - SOLICITUD_PRECIO
    - SOLICITUD_CITA
    - QUEJA
    - INDECISO

    Mensaje: {mensaje}

    Devuelve SOLO la categoría.
    """

    respuesta = llamar_a_ollama(prompt)
    return respuesta.strip()
