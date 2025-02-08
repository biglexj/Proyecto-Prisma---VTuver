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
import rapidfuzz

# Ruta del archivo JSON con la personalidad de Ely
ruta = "data/ely_personality.json"

# Cargar el JSON con la rule
with open(ruta, "r", encoding="utf-8") as archivo:
    ely_personality = json.load(archivo)

with open("data/ely_rules.json", "r", encoding="utf-8") as file:
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

# Entrada de YouTube Live
imput_YT = "que haces en youtube"  # Esta es la pregunta que se hace


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


# Llamar a la función para obtener la respuesta correcta
respuesta = rule_resultado(imput_YT)

# Preparar el mensaje del prompt combinando el contexto y la respuesta
# El prompt contiene toda la información relevante: personalidad de Ely, respuesta y la pregunta
# Crear el prompt explícito
prompt = (
    f"Tu personalidad es la siguiente: {ely_personality_text}\n"  # Se define claramente la personalidad de Ely
    f"La pregunta que te hacen es: {imput_YT}\n"  # Contexto de la pregunta del usuario
    f"Tu respuesta debe ser breve, concisa y acorde a tu personalidad.\n"  # Instrucción clara
    f"Responde como {ely_personality['nombre']} y asegúrate de mantener tu tono característico.\n"
)


# Llama al modelo de Ollama
response = ollama.chat(
    model="llama3.2",
    messages=[
        {"role": "user", "content": prompt}
    ]
)
response["message"]["content"]

generated_text = response["message"]["content"]  # Obtén el texto generado

print("Ely VTuber:", generated_text)  # Imprime la respuesta generada


# Verificar que el archivo de modelo de voz existe
file_path = "model_voz/cloning/Ely_model.wav"
if os.path.exists(file_path):
    print(f"El archivo '{file_path}' existe y está listo para usarse.")
else:
    raise FileNotFoundError(f"El archivo '{file_path}' no se encuentra. Verifica la ruta.")


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

def agregar_contexto(texto):
    if len(contexto) > 10:  # Limitar la memoria
        contexto.pop(0)
    contexto.append(texto)

def obtener_contexto():
    return " ".join(contexto)

# Definir la función principal para el chat
def main():
    url = "https://www.youtube.com/watch?v=f6Nw2W5vQXo"
    chat = ChatDownloader().get_chat(url)
    
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