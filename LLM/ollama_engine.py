import ollama as ollama
import re
import httpx
import time

def ollama_engine(chat_text, personality_text, rule_resultado, retries=3):
    prompt = (
        f"Tu personalidad es la siguiente: {personality_text}\n"
        f"La pregunta que te hacen es: {chat_text}\n"
        f"Tener en cuenta ciertos mensajes y tomar con cautela: {rule_resultado}\n"
        f"Tu respuesta debe ser breve, concisa y acorde a tu personalidad.\n"
        f"Evita decir te ayudare en algo, porque eres una VTuber y enfocada en la interacción con el público del live."
    )
    
    for attempt in range(retries):
        try:
            response = ollama.chat(
                model="deepseek-r1:1.5b",
                messages=[{"role": "user", "content": prompt}]
            )
            generated_text = response["message"]["content"]
            filtered_text = re.sub(r'<think>.*?</think>', '', generated_text, flags=re.DOTALL).strip()
            return filtered_text
        except httpx.RequestError as e:
            print(f"✗ Error de solicitud HTTP (intento {attempt + 1}): {e}")
            time.sleep(2)  # Esperar antes de reintentar
        except Exception as e:
            print(f"✗ Error al obtener la respuesta de Ollama (intento {attempt + 1}): {e}")
            time.sleep(2)  # Esperar antes de reintentar
    return None
 