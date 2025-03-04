import pyttsx3

# Función para la síntesis de voz con pyttsx3

def speak(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"✗ Error al reproducir el texto: {e}")