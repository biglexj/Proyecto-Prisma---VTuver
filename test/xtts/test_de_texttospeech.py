from TTS.api import TTS

tts = TTS("tts_models/en/ljspeech/fast_pitch").to("cuda")  # Usa FastPitch, basado en FastSpeech2
tts.tts_to_file(text="Hola, este es un ejemplo de FastSpeech 2.", file_path="output.wav")
