from chat_downloader import ChatDownloader
import test.ollama as ollama
import torch
from TTS.api import TTS
import sounddevice as sd
import numpy as np
import os
import json
import random
import re
from rapidfuzz import process  # Se usa en la función rule_resultado para encontrar coincidencias

# Ruta del archivo JSON con la personalidad de Ely
ruta = "data/ely_personality.json"

# Cargar el JSON con la rule
try:
    with open(ruta, "r", encoding="utf-8") as archivo:
        ely_personality = json.load(archivo)
except FileNotFoundError:
    raise FileNotFoundError(f"El archivo '{ruta}' no se encuentra. Verifica la ruta.")
except json.JSONDecodeError:
    raise ValueError(f"El archivo '{ruta}' no es un JSON válido.")

try:
    with open("data/ely_rules.json", "r", encoding="utf-8") as file:
        ely_rules = json.load(file)
except FileNotFoundError:
    raise FileNotFoundError("El archivo 'data/ely_rules.json' no se encuentra. Verifica la ruta.")
except json.JSONDecodeError:
    raise ValueError("El archivo 'data/ely_rules.json' no es un JSON válido.")

ely_personality_text = (
    "Nombre: " + ely_personality["nombre"] + "\n" +
    "Personalidad: " + ely_personality["personalidad"] + "\n" +
    "Estilo Visual: " + ely_personality["estilo_visual"] + "\n" +
    "Interacciones: " + ely_personality["interacciones"] + "\n" +
    "Habilidades: " + ely_personality["habilidades"] + "\n" +
    "Tono de voz: " + ely_personality["tono_de_voz"] + "\n" +
    "Misión: " + ely_personality["mision"] + "\n" +
    "Bienvenida: " + ely_personality["bienvenida"] + "\n" +
    "Despedida: " + ely_personality["despedida"] + "\n" +
    "Humor: " + ely_personality["humor"]
)

# Función para buscar una respuesta
def rule_resultado(chat_YT):
    for clave, valor in ely_rules.items():
        if "pregunta" in valor:
            match = process.extractOne(chat_YT, valor["pregunta"])
            if match and match[1] > 80:
                if "respuesta_1" in valor:
                    return random.choice([valor["respuesta_1"], valor["respuesta_2"]])
                return valor["respuesta"]
    return "Toma un criterio neutral a las preguntas con un poco de sarcasmo de vez en cuando."

# Carga el modelo de Coqui TTS
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Usando dispositivo: {device}")
try:
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
except Exception as e:
    raise RuntimeError(f"Error al cargar el modelo TTS: {e}")

# Generar audio directamente y reproducirlo
def synthesize_and_play_immediately(filtered_text, speaker_path, language="es"):
    try:
        # Generar la forma de onda directamente desde el modelo TTS
        audio_waveform = tts.tts(
            text=filtered_text, 
            speaker_wav=speaker_path, 
            language=language
        )
        
        # Normalizar la señal de audio
        audio_waveform = np.array(audio_waveform, dtype=np.float32)
        audio_waveform /= np.max(np.abs(audio_waveform))
        
        # Configurar la frecuencia de muestreo (asegúrate de usar la misma frecuencia que el modelo)
        samplerate = 22050  # Cambia este valor si tu modelo usa una frecuencia diferente
        
        # Reproducir el audio
        sd.play(audio_waveform, samplerate)
        sd.wait()  # Esperar hasta que termine la reproducción
    except Exception as e:
        print(f"✗ Error al sintetizar y reproducir el audio: {e}")

contexto = []
def agregar_contexto(texto):
    if len(contexto) > 10:  # Limitar la memoria
        contexto.pop(0)
    contexto.append(texto)

def obtener_contexto():
    return " ".join(contexto)

# Definir la función principal para el chat
def main():
    url = "https://www.youtube.com/watch?v=f6Nw2W5vQXo"
    try:
        chat = ChatDownloader().get_chat(url)
    except Exception as e:
        raise RuntimeError(f"Error al conectar con el chat de YouTube: {e}")
    
    for chat_YT in chat:
        message = chat_YT.get('message', '')
        author_name = chat_YT.get('author', {}).get('name', 'Desconocido')
        
        if message:
            chat_text = author_name + ": " + message
            print(chat_text)
            resultado = rule_resultado(message)
            response = ollama_engine(chat_text, ely_personality_text, resultado)
            
            if response:
                filtered_text = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL).strip()
                print("Ely VTuber:", filtered_text)

                # Definir la ruta del archivo de modelo de voz
                speaker_path = "model_voz/cloning/Ely_model.wav"

                # Verificar que el archivo de modelo de voz existe
                if not os.path.exists(speaker_path):
                    raise FileNotFoundError(f"El archivo '{speaker_path}' no se encuentra. Verifica la ruta.")

                # Llamar a la función para sintetizar y reproducir
                synthesize_and_play_immediately(filtered_text, speaker_path=speaker_path)

# Función para obtener la respuesta de Ollama
def ollama_engine(chat_text, personality_text, rule_resultado):
    prompt = (
        f"Tu personalidad es la siguiente: {personality_text}\n"
        f"La pregunta que te hacen es: {chat_text}\n"
        f"Tener en cuenta ciertos mensajes y tomar con cautela: {rule_resultado}\n"
        f"Tu respuesta debe ser breve, concisa y acorde a tu personalidad.\n"
        f"Evita decir te ayudare en algo, porque eres una VTuber y enfocada en la interacción con el público del live."
    )
    
    try:
        response = ollama.chat(
            model="deepseek-r1:1.5b",
            messages=[{"role": "user", "content": prompt}]
        )
        generated_text = response["message"]["content"]
        filtered_text = re.sub(r'<think>.*?</think>', '', generated_text, flags=re.DOTALL).strip()
        return filtered_text
    except Exception as e:
        print(f"✗ Error getting Ollama response: {e}")
        return None

if __name__ == "__main__":
    main()