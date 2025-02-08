from chat_downloader import ChatDownloader
import torch
from TTS.api import TTS
import sounddevice as sd
import numpy as np
from scipy.io import wavfile


generated_text = "Es es una prueba de idioma ¿que? no se"


print("Ely VTuber:", generated_text)  # Imprime la respuesta generada

# Carga el modelo de Coqui TTS
device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

texto = generated_text
#texto = texto.replace("¿", "").replace("¡", "") el modelo xtts si soporta.

# Generar y guardar el archivo de audio
wav = tts.tts(text= texto, speaker_wav="../../model_voz/cloning/Ely_model.wav", language="es")
# Text to speech to a file
tts.tts_to_file(text= texto, speaker_wav="../../ymodel_voz/cloning/Ely_model.wav", language="es", file_path="output.wav")

# Reproducir el archivo generado con sounddevice
def play_audio(file_path):
    # Leer el archivo WAV con scipy.io.wavfile
    sample_rate, audio_data = wavfile.read(file_path)
    
    # Reproducir el audio utilizando sounddevice
    sd.play(audio_data, sample_rate)
    sd.wait()  # Esperar hasta que termine la reproducción

# Llamar a la función para reproducir el archivo de audio
play_audio("output.wav")