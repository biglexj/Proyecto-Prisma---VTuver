def ollama_engine(chat_text, personality_text, rule_resultado, retries=3):
    prompt = (
        f"Tu personalidad es la siguiente: {personality_text}\n"
        f"La pregunta que te hacen es: {chat_text}\n"
        f"Tener en cuenta ciertos mensajes y tomar con cautela: {rule_resultado}\n"
        f"Tu respuesta debe ser breve, concisa y acorde a tu personalidad.\n"
        f"Evita decir te ayudare en algo, porque eres una VTuber y enfocada en la interacción con el público del live."
    )