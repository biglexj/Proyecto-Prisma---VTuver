from TTS.api import TTS
import torch

# Verificar si se está utilizando GPU o CPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Usando dispositivo: {device}")

# Cargar el modelo TTS
try:
    tts = TTS("tts_models/es/mai/tacotron2-DDC").to(device)
    print("Modelo TTS cargado exitosamente.")
except Exception as e:
    print(f"✗ Error al cargar el modelo TTS: {e}")

# Generar y guardar el archivo de audio
try:
    tts.tts_to_file(text="Hola, este es un ejemplo de voz en español que esta en esta pc.", file_path="output.wav")
    print("Archivo de audio generado exitosamente.")
except Exception as e:
    print(f"✗ Error al generar el archivo de audio: {e}")
