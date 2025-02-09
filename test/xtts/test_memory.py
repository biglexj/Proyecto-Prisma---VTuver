from chat_downloader import ChatDownloader
import test.ollama as ollama
import torch
from TTS.api import TTS
import sounddevice as sd
import numpy as np
from scipy.io import wavfile
import json
from rapidfuzz import process  # Se usa en la función rule_resultado para encontrar coincidencias
import random

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
# Entrada de YouTube Live
chat_YT = "que haces en youtube"  # Esta es la pregunta que se hace

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
respuesta = rule_resultado(chat_YT)

# Preparar el mensaje del prompt combinando el contexto y la respuesta
# El prompt contiene toda la información relevante: personalidad de Ely, respuesta y la pregunta
# Crear el prompt explícito
prompt = (
    f"Tu personalidad es la siguiente: {ely_personality_text}\n"  # Se define claramente la personalidad de Ely
    f"La pregunta que te hacen es: {chat_YT}\n"  # Contexto de la pregunta del usuario
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
