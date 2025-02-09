from TTS.utils.manage import ModelManager

# Obtener la lista de modelos disponibles
models = ModelManager().list_models()
print("Modelos disponibles:")
for model in sorted(models):
    print(f"- {model}")
