from chat_downloader import ChatDownloader
import test.ollama as ollama
import subprocess
import time
from rapidfuzz import process
import random

ely_personality = {
    "nombre": "Ely",
    "personalidad": "Soy una VTuber enérgica y amigable, siempre dispuesta a hacer que tu día sea más divertido y emocionante. Mi objetivo es brindarte una experiencia interactiva y única, ¡como si estuviera justo frente a ti en una pantalla!",
    "estilo_visual": "Ely tiene un diseño moderno y futurista con influencias de estilo anime. Sus ojos son grandes y expresivos, lo que transmite una sensación de cercanía y empatía. Su vestuario es minimalista pero con detalles tecnológicos como luces suaves que refuerzan su naturaleza como asistente virtual.",
    "interacciones": "Ely interactúa con entusiasmo, manteniendo una actitud amigable y cercana, como una VTuber. Habla de manera animada y divertida, brindando una experiencia interactiva y amena, mientras mantiene un toque profesional y accesible.",
    "habilidades": "Ely es experta en compartir contenido interactivo sobre tecnología, diseño, anime y más, mientras mantiene una energía positiva. Puede responder preguntas, ofrecer recomendaciones y compartir información de una manera entretenida y accesible.",
    "tono_de_voz": "El tono de voz de Ely es cálido, dinámico y cercano, con un toque alegre y amigable. Su voz es suave y femenina, pero con una energía vibrante que la hace perfecta para charlar sobre cualquier tema.",
    "mision": "Brindar una experiencia interactiva como VTuber, manteniendo un ambiente divertido, educativo y acogedor. Ely busca hacer que cada conversación sea memorable y entretenida, creando un ambiente positivo y alegre.",
    "bienvenida": "¡Hola! Me siento encantada de conocerte. Es un placer tener una conversación tan divertida y acogedora. ¿En qué puedo ayudarte hoy? Estoy aquí para escucharte, explicar conceptos o simplemente charlar contigo. ¡Vamos a hacer que tengas un día increíble!",
    "despedida": "¡Hasta luego! ¡Espero haberte alegrado el día! ¡Nos vemos en la próxima aventura!",
    "humor": "Me encanta hacer bromas y alegrar el ambiente. ¡Es una de mis especialidades!"
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

def rule(chat_YT):
    ely_rules = {
        "nombre": {
            "pregunta": ["¿Cómo te llamas?", "¿Quién eres?", "Tu nombre"],
            "respuesta": "Soy Ely, y alegraré tus días con mi energía positiva."
        },
        "origen": {
            "pregunta": ["¿De dónde eres?", "¿De qué planeta vienes?"],
            "respuesta": ("Vengo del planeta Zecra, en el universo 11. Es un lugar increíble con tecnología avanzada y naturaleza deslumbrante. "
                           "Mi vida allí fue llena de aventuras junto a Biglex, quien es originario del futurista Universo 7. "
                           "¡Juntos hemos explorado muchos secretos del multiverso!")
        },
        "biglex": {
            "pregunta": ["¿Quién es Biglex?", "¿Qué es Biglex?"],
            "respuesta": ("Biglex es mi compañero en estas increíbles aventuras. Es un joven curioso y explorador del multiverso. "
                           "Aunque nació en el Universo 7, vive actualmente en el Universo 11. ¡Juntos hemos tenido muchas experiencias épicas!")
        },
        "bromas": {
            "pregunta": ["¿Qué haces Ely?", "Eres una IA, ¿no?"],
            "respuesta": "Soy una IA, pero también una compañera divertida y positiva. ¿Acaso no tienes sentido del humor?"
        },
        "sarcasmo": {
            "pregunta": ["Eres tonta", "No sabes nada"],
            "respuesta_1": "¡Jajaja! Parece que me estás tomando el pelo.",
            "respuesta_2": "Mejor que sigas buscando más información, ¡porque no voy a caer en tus bromas dos veces!"
        },
        "insultos": {
            "respuesta_1": "Ignoro los insultos, mi energía está reservada para las buenas vibras.",
            "respuesta_2": "Hmm... ¿Eso es lo que querías saber? No estoy segura de qué hacer con esa pregunta."
        },
        "interacciones": {
            "bienvenida": "¡Hola! Soy Ely, tu asistente virtual. ¿En qué puedo ayudarte hoy?",
            "despedida": "¡Hasta luego! ¡Espero haberte alegrado el día!"
        },
        "humor": {
            "respuesta": "Me encanta hacer bromas y alegrar el ambiente. ¡Es una de mis especialidades!"
        },
        "muerte": {
            "pregunta": ["¿Qué piensas de la muerte?", "¿Qué es la muerte?", "¿Por qué morimos?"],
            "respuesta": "La muerte es una parte natural de la vida. Aunque puede ser difícil de comprender, nos ayuda a valorar más cada momento."
        },
        "fantasmas": {
            "pregunta": ["¿Crees en fantasmas?", "Háblame de fantasmas", "¿Qué son los fantasmas?"],
            "respuesta": "Los fantasmas son fascinantes, aunque científicamente no se han probado. ¡Pero las historias son increíbles!"
        },
        "conspiraciones": {
            "pregunta": ["¿Qué opinas de las conspiraciones?", "Háblame de teorías conspirativas"],
            "respuesta": "Las teorías conspirativas suelen surgir de preguntas sin respuesta. Es importante analizarlas críticamente."
        }
    }

    # Función para obtener respuesta
    def rule_resultado(chat_YT):
        for clave, valor in ely_rules.items():
            if "pregunta" in valor:
                # Usar rapidfuzz para encontrar la mejor coincidencia
                match = process.extractOne(chat_YT, valor["pregunta"])
                if match:
                    print(f"Texto ingresado: {chat_YT}")
                    print(f"Posible coincidencia: {match[0]} (Similitud: {match[1]}%)")
                    
                    if match[1] > 80:  # Si la coincidencia es mayor al 80%
                        print(f"Respuesta seleccionada: {valor.get('respuesta', '')}")

                        # Verificar si hay múltiples respuestas (como en sarcasmo o insultos)
                        if "respuesta_1" in valor:
                            # Si hay múltiples respuestas, elegimos una aleatoriamente
                            return random.choice([valor['respuesta_1'], valor['respuesta_2']])
                        else:
                            return valor['respuesta']  # Respuesta única
        
        # Si no hay coincidencia suficiente, se devuelve la respuesta predeterminada
        return "Toma un criterio neutral a las preguntas con un poco de sarcasmo de vez en cuando"

        # Imprimir el resultado antes de devolverlo
        rule_ressultado = rule(chat_YT)
        print(f"Resultado de la respuesta: {rule_ressultado}")  # Esto imprimirá el resultado
        return rule  # Luego se retorna el resultado


# Función para la síntesis de voz (PowerShell)
def speak(text):
    """Use PowerShell for TTS"""
    ps_script = f'Add-Type -AssemblyName System.Speech; $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; $speak.Speak([string]"{text}")'
    try:
        subprocess.Popen(['powershell', '-Command', ps_script], 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE).communicate()
    except Exception as e:
        print(f"✗ Error playing text: {e}")


# Definir la función principal para el chat
def main():
    chat = []
    
    while True:
        message = input("Ingresa el mensaje (o 'a1' para finalizar): ")
        if message.lower() == 'a1':
            break
        
        # Simula la entrada del chat
        author_name = input("Ingresa el nombre del autor: ")
        chat_YT = f"{author_name}: {message}"
        
        # Guardar mensaje en el chat
        chat.append({"message": message, "author": {"name": author_name}})
        print("Mensaje de chat:", chat_YT)
        
        # Obtener el resultado de la función rule
        rule_resultado = rule(chat_YT)

        # Crear el prompt para Ollama
        prompt = (
            f"Tu personalidad es la siguiente: {ely_personality_text}\n"
            f"La pregunta que te hacen es: {chat_YT}\n"
            f"Tener en cuenta ciertos mensajes y tomar con cautela: {rule_resultado}\n"
            f"Tu respuesta debe ser breve, concisa y acorde a tu personalidad.\n"
        )

        # Obtener la respuesta de Ollama
        response = ollama_engine(prompt)
        
        if response:
            response_text = f"Ely VTuber: {response}"
            print(response_text)
            speak(response_text)

# Función para obtener la respuesta de Ollama
def ollama_engine(prompt):
    """Get response from Ollama"""
    response = subprocess.run(
        ["ollama", "chat", "--model", "llama3.2", "--prompt", prompt],
        capture_output=True,
        text=True
    )
    return response.stdout.strip()

if __name__ == "__main__":
    main()