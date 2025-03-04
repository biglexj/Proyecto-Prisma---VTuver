from chat_downloader import ChatDownloader
from chat_downloader.errors import ParsingError
import re
import time
import pyttsx3
from context.ely_personality import load_personality
from context.ely_rules import load_rules, rule_resultado
from LLM.ollama_engine import ollama_engine

def chat_loop():
    url = "https://www.youtube.com/live/FqrJOatiruE"
    try:
        chat = ChatDownloader().get_chat(url, timeout=10)
    except ParsingError as e:
        print(f"✗ Error parsing video data: {e}")
        return

    processed_messages = set()  # Conjunto para almacenar mensajes procesados
    
    ely_personality_text = load_personality()
    ely_rules = load_rules()

    while True:
        for chat_YT in chat:
            try:
                message_id = chat_YT.get('id')
                if message_id not in processed_messages:
                    processed_messages.add(message_id)
                    message = chat_YT.get('message', '')
                    author_name = chat_YT.get('author', {}).get('name', 'Desconocido')
                    
                    if message:
                        chat_text = author_name + ": " + message
                        print(chat_text)
                        resultado = rule_resultado(message, ely_rules)
                        response = ollama_engine(chat_text, ely_personality_text, resultado)
                        
                        if response:
                            filtered_text = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL).strip()
                            print("Ely VTuber:", filtered_text)
                            speak(filtered_text)
            except Exception as e:
                print(f"✗ Error processing message: {e}")
        
        # Verificar si se ha escrito "salir" en la consola
        if input("Escribe 'salir' para finalizar: ").strip().lower() == 'salir':
            break

        time.sleep(1)  # Esperar un segundo antes de verificar nuevos mensajes

def speak(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"✗ Error al reproducir el texto: {e}")

if __name__ == "__main__":
    try:
        chat_loop()
    except KeyboardInterrupt:
        print("Programa interrumpido por el usuario.")
    except Exception as e:
        print(f"✗ Error inesperado: {e}")
    finally:
        print("Programa finalizado.")