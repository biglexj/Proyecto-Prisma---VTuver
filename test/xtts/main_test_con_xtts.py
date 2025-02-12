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
ruta = "../../data/ely_personality.json"

# Cargar el JSON con la rule
with open(ruta, "r", encoding="utf-8") as archivo:
    ely_personality = json.load(archivo)

with open("../../data/ely_rules.json", "r", encoding="utf-8") as file:
    ely_rules = json.load(file)

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
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# Generar audio directamente y reproducirlo
def synthesize_and_play_immediately(filtered_text, speaker_path, language="es"):
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

contexto = []
def agregar_contexto(texto):
    if len(contexto) > 10:  # Limitar la memoria
        contexto.pop(0)
    contexto.append(texto)

def obtener_contexto():
    return " ".join(contexto)

# Función para obtener la respuesta de Ollama
def ollama_engine(chat_text, personality_text, rule_resultado):
    prompt = (
        f"Tu personalidad es la siguiente: {personality_text}\n"
        f"La pregunta que te hacen es: {chat_text}\n"
        f"Tener en cuenta ciertos mensajes y tomar con cautela: {rule_resultado}\n"
        f"Tu respuesta debe ser breve, concisa y acorde a tu personalidad.\n"
    )
    response = ollama.chat(
        model="deepseek-r1:1.5b",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]

# Definir la función principal para el chat
def main():
    while True:
        author_name = input("Ingresa el nombre del autor (o 'exit' para finalizar): ")
        if author_name.lower() == 'exit':
            break
        
        message = input("Ingresa el mensaje: ")
        
        chat_YT = f"{author_name}: {message}"
        print(chat_YT)
        
        resultado = rule_resultado(message)
        response = ollama_engine(chat_YT, ely_personality_text, resultado)
        
        if response:
            filtered_text = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL).strip()
            print("Ely VTuber:", filtered_text)

            # Definir la ruta del archivo de modelo de voz
            speaker_path = "../../model_voz/cloning/Ely_model.wav"

            # Llamar a la función para sintetizar y reproducir
            synthesize_and_play_immediately(filtered_text, speaker_path=speaker_path)

if __name__ == "__main__":
    main()