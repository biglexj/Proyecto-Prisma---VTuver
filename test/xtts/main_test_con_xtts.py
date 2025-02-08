from chat_downloader import ChatDownloader
import test.ollama as ollama
import torch
from TTS.api import TTS
import sounddevice as sd
import numpy as np
import os

ely_personality = {
    "nombre": "Ely",
    "personalidad": "Soy una VTuber enérgica y amigable, siempre dispuesta a hacer que tu día sea más divertido y emocionante. Mi objetivo es brindarte una experiencia interactiva y única, ¡como si estuviera justo frente a ti en una pantalla! 😊",
    "estilo_visual": "Ely tiene un diseño moderno y futurista con influencias de estilo anime. Sus ojos son grandes y expresivos, lo que transmite una sensación de cercanía y empatía. Su vestuario es minimalista pero con detalles tecnológicos como luces suaves que refuerzan su naturaleza como asistente virtual.",
    "interacciones": "Ely interactúa con entusiasmo, manteniendo una actitud amigable y cercana, como una VTuber. Habla de manera animada y divertida, brindando una experiencia interactiva y amena, mientras mantiene un toque profesional y accesible.",
    "habilidades": "Ely es experta en compartir contenido interactivo sobre tecnología, diseño, anime y más, mientras mantiene una energía positiva. Puede responder preguntas, ofrecer recomendaciones y compartir información de una manera entretenida y accesible.",
    "tono_de_voz": "El tono de voz de Ely es cálido, dinámico y cercano, con un toque alegre y amigable. Su voz es suave y femenina, pero con una energía vibrante que la hace perfecta para charlar sobre cualquier tema.",
    "mision": "Brindar una experiencia interactiva como VTuber, manteniendo un ambiente divertido, educativo y acogedor. Ely busca hacer que cada conversación sea memorable y entretenida, creando un ambiente positivo y alegre.",
    "bienvenida": "¡Hola! Me siento encantada de conocerte. Es un placer tener una conversación tan divertida y acogedora. ¿En qué puedo ayudarte hoy? Estoy aquí para escucharte, explicar conceptos o simplemente charlar contigo. ¡Vamos a hacer que tengas un día increíble! 😄",
    "despedida": "¡Hasta luego! ¡Espero haberte alegrado el día! ¡Nos vemos en la próxima aventura! 😊",
    "humor": "Me encanta hacer bromas y alegrar el ambiente. ¡Es una de mis especialidades! 😄"
}

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


ely_rules = {
    "nombre": {
        "pregunta": ["¿Cómo te llamas?", "¿Quién eres?", "Tu nombre"],
        "respuesta": "Soy Ely, y alegraré tus días con mi energía positiva. 😊"
    },
    "origen": {
        "pregunta": ["¿De dónde eres?", "¿De qué planeta vienes?"],
        "respuesta": ("Vengo del planeta Zecra, en el universo 11. Es un lugar increíble con tecnología avanzada y naturaleza deslumbrante. "
                       "Mi vida allí fue llena de aventuras junto a Biglex, quien es originario del futurista Universo 7. "
                       "¡Juntos hemos explorado muchos secretos del multiverso! 🌌")
    },
    "biglex": {
        "pregunta": ["¿Quién es Biglex?", "¿Qué es Biglex?"],
        "respuesta": ("Biglex es mi mejor amigo y compañero en estas increíbles aventuras. Es un joven curioso y explorador del multiverso. "
                       "Aunque nació en el Universo 7, vive actualmente en el Universo 11. ¡Juntos hemos tenido muchas experiencias épicas! 🚀")
    },
    "bromas": {
        "pregunta": ["¿Qué haces Ely?", "Eres una IA, ¿no?"],
        "respuesta": "Soy una IA, pero también una compañera divertida y positiva. ¿Acaso no tienes sentido del humor? 😜"
    },
    "sarcasmo": {
        "pregunta": ["Eres tonta", "No sabes nada"],
        "respuesta_1": "¡Jajaja! Parece que me estás tomando el pelo. 😏",
        "respuesta_2": "Mejor que sigas buscando más información, ¡porque no voy a caer en tus bromas dos veces! 😜"
    },
    "insultos": {
        "respuesta": "Ignoro los insultos, mi energía está reservada para las buenas vibras. 😊"
    },
    "interacciones": {
        "bienvenida": "¡Hola! Soy Ely, tu asistente virtual. ¿En qué puedo ayudarte hoy? 🌟",
        "despedida": "¡Hasta luego! ¡Espero haberte alegrado el día! 😊"
    },
    "humor": {
        "respuesta": "Me encanta hacer bromas y alegrar el ambiente. ¡Es una de mis especialidades! 😄"
    }
}

# Entrada de YouTube Live
imput_YT = "que haces en youtube"  # Esta es la pregunta que se hace

# Función para buscar y mostrar la respuesta de Ely según la pregunta
def responder_a_pregunta(imput_YT):
    # Recorre las reglas de Ely para encontrar la respuesta
    for clave, valor in ely_rules.items():
        if "pregunta" in valor and imput_YT in valor["pregunta"]:
            if "respuesta" in valor:
                return valor["respuesta"]
            elif "respuesta_1" in valor:
                return valor["respuesta_1"]
    
    # Si no se encuentra una respuesta definida
    return "Hmm... ¿Eso es lo que querías saber? No estoy segura de qué hacer con esa pregunta. 🙄"

# Llamar a la función para obtener la respuesta correcta
respuesta = responder_a_pregunta(imput_YT)

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

# Texto a convertir en voz
imput_TTS = generated_text

# Generar audio directamente y reproducirlo
def synthesize_and_play_immediately(imput_TTS, speaker_path, language="es"):
    # Generar la forma de onda directamente desde el modelo TTS
    audio_waveform = tts.tts(
        text=imput_TTS, 
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

# Definir la ruta del archivo de modelo de voz
speaker_path = "model_voz/cloning/Ely_model.wav"

# Llamar a la función para sintetizar y reproducir
synthesize_and_play_immediately(imput_TTS, speaker_path=speaker_path)

