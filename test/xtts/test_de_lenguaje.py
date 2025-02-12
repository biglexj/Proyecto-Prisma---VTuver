from chat_downloader import ChatDownloader
import torch
from TTS.api import TTS
import sounddevice as sd
from scipy.io import wavfile

generated_text = "Es es una prueba de idioma ¿que? no se"

print("Ely VTuber:", generated_text)  # Imprime la respuesta generada

# Carga el modelo de Coqui TTS
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Usando dispositivo: {device}")

try:
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    print("Modelo TTS cargado exitosamente.")
except Exception as e:
    print(f"✗ Error al cargar el modelo TTS: {e}")

texto = generated_text

# Generar y guardar el archivo de audio
try:
    wav = tts.tts(text=texto, speaker_wav="../../model_voz/cloning/Ely_model.wav", language="es")
    tts.tts_to_file(text=texto, speaker_wav="../../model_voz/cloning/Ely_model.wav", language="es", file_path="output.wav")
    print("Archivo de audio generado exitosamente.")
except Exception as e:
    print(f"✗ Error al generar el archivo de audio: {e}")

# Reproducir el archivo generado con sounddevice
def play_audio(file_path):
    try:
        # Leer el archivo WAV con scipy.io.wavfile
        sample_rate, audio_data = wavfile.read(file_path)
        
        # Reproducir el audio utilizando sounddevice
        sd.play(audio_data, sample_rate)
        sd.wait()  # Esperar hasta que termine la reproducción
        print("Reproducción de audio completada.")
    except FileNotFoundError:
        print(f"✗ El archivo '{file_path}' no se encuentra. Verifica la ruta.")
    except Exception as e:
        print(f"✗ Error al reproducir el archivo de audio: {e}")

# Llamar a la función para reproducir el archivo de audio
play_audio("output.wav")